"""
Tencent provider implementation for Hunyuan and LKEAP LLM models

This module implements the Provider interface for Tencent's Hunyuan and LKEAP models.
It supports both streaming and non-streaming completions, as well as image inputs.
"""
from typing import Optional, Union, AsyncGenerator, Dict, Any, List
import base64
import json
import mimetypes
from pathlib import Path

from tencentcloud.common import credential
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.hunyuan.v20230901 import hunyuan_client, models as hunyuan_models
from tencentcloud.lkeap.v20240522 import lkeap_client, models as lkeap_models

from llm_cli.providers.base import Provider, register_provider

class BaseTencentProvider(Provider):
    """Base class for Tencent API providers"""
    
    def __init__(self):
        """Initialize the provider"""
        self._default_config = {
            'temperature': 1.0,
            'top_p': 1.0,
        }
        
    def _get_credentials(self, api_key: Dict[str, str]) -> credential.Credential:
        """Get credentials from API key dict"""
        secret_id = api_key.get('secret_id')
        secret_key = api_key.get('secret_key')
        
        if not secret_id or not secret_key:
            raise ValueError("API key must contain both 'secret_id' and 'secret_key'")
            
        return credential.Credential(secret_id, secret_key)

    def _get_mime_type(self, file_path: str) -> str:
        """Get MIME type for a file."""
        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type or not mime_type.startswith('image/'):
            return 'image/jpeg'  # Default to JPEG
        return mime_type

    def _load_image(self, image_path: str) -> tuple[bytes, str]:
        """Load image file as bytes and get its MIME type."""
        with open(image_path, 'rb') as f:
            return f.read(), self._get_mime_type(image_path)

    def _format_search_results(self, data: dict) -> str:
        """Format search results into a readable string."""
        if not data or 'SearchInfo' not in data or not data['SearchInfo'] or 'SearchResults' not in data['SearchInfo']:
            return ""
            
        search_results = data['SearchInfo']['SearchResults']
        if not search_results:
            return ""
            
        output = "\n\nSources:\n"
        for result in search_results:
            index = result.get('Index', 0)
            title = result.get('Title', 'Untitled')
            url = result.get('Url', '')
            site = result.get('Text', '')
            
            output += f"[{index}] {title}\n"
            if url:
                output += f"    URL: {url}\n"
            if site:
                output += f"    Site: {site}\n"
            output += "\n"
            
        return output

@register_provider("tencent")
class TencentProvider(BaseTencentProvider):
    """Tencent API provider for Hunyuan LLM models"""

    def __init__(self):
        super().__init__()
        self._region = "ap-beijing"  # Default region for Hunyuan

    def _is_deepseek_model(self, model: str) -> bool:
        """Check if the model is a deepseek model"""
        return model.startswith("deepseek")

    def _create_chat_request(
        self,
        prompt: str,
        model: str,
        temperature: float = 1.0,
        top_p: float = 1.0,
        stream: bool = True,
        web_search: bool = False
    ) -> hunyuan_models.ChatCompletionsRequest:
        """Create a chat request."""
        req = hunyuan_models.ChatCompletionsRequest()
        req.Model = model
        req.Stream = stream
        req.Temperature = temperature
        req.TopP = top_p
        
        # Enable web search enhancements
        if web_search:
            req.ForceSearchEnhancement = True
            req.Citation = True
            req.SearchInfo = True
        
        # Create message
        message = hunyuan_models.Message()
        message.Role = "user"
        message.Content = prompt
        req.Messages = [message]
        
        return req

    def _create_vision_request(
        self,
        prompt: str,
        image_path: str,
        model: str = "hunyuan-standard-vision",
        temperature: float = 1.0,
        top_p: float = 1.0
    ) -> hunyuan_models.ChatCompletionsRequest:
        """Create a vision request."""
        req = hunyuan_models.ChatCompletionsRequest()
        req.Model = model
        req.Stream = False  # Vision doesn't support streaming
        req.Temperature = temperature
        req.TopP = top_p
        
        # Create system message
        system_msg = hunyuan_models.Message()
        system_msg.Role = "system"
        system_msg.Content = "You are a helpful assistant."
        
        # Create user message with image
        user_msg = hunyuan_models.Message()
        user_msg.Role = "user"
        
        # Create image content
        image_content = hunyuan_models.Content()
        image_content.Type = "image_url"
        image_content.Text = "The picture is taken by the user."
        
        # Load and encode image
        image_bytes, mime_type = self._load_image(image_path)
        image_base64 = base64.b64encode(image_bytes).decode()
        
        image_url = hunyuan_models.ImageUrl()
        image_url.Url = f"data:{mime_type};base64,{image_base64}"
        image_content.ImageUrl = image_url
        
        # Create text content
        text_content = hunyuan_models.Content()
        text_content.Type = "text"
        text_content.Text = prompt
        
        # Set contents
        user_msg.Contents = [image_content, text_content]
        
        req.Messages = [system_msg, user_msg]
        return req

    async def complete(
        self,
        prompt: str,
        model: str,
        api_key: Dict[str, str],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        image_paths: Optional[List[str]] = None,
        web_search: bool = False,
        **kwargs: Dict[str, Any]
    ) -> Union[str, AsyncGenerator[str, None]]:
        """Complete a prompt using Tencent's API
        
        This is a router function that delegates to either Hunyuan or LKEAP provider
        based on the model name.
        """
        if self._is_deepseek_model(model):
            provider = LkeapProvider()
            return await provider.complete(
                prompt=prompt,
                model=model,
                api_key=api_key,
                temperature=temperature,
                max_tokens=max_tokens,
                image_paths=image_paths,
                web_search=web_search,
                **kwargs
            )
            
        # Continue with Hunyuan implementation
        try:
            # Initialize client
            cred = self._get_credentials(api_key)
            client = hunyuan_client.HunyuanClient(cred, self._region)
            
            # Handle vision request
            if image_paths and len(image_paths) > 0:
                if len(image_paths) > 1:
                    raise ValueError("Hunyuan only supports one image per request")
                    
                req = self._create_vision_request(
                    prompt=prompt,
                    image_path=image_paths[0],
                    model=model,
                    temperature=temperature,
                    top_p=kwargs.get('top_p', self._default_config['top_p'])
                )
                response = client.ChatCompletions(req)
                return response.Choices[0].Message.Content
            
            # Handle text chat request
            req = self._create_chat_request(
                prompt=prompt,
                model=model,
                temperature=temperature,
                top_p=kwargs.get('top_p', self._default_config['top_p']),
                stream=True,
                web_search=web_search
            )
            
            async def stream_response() -> AsyncGenerator[str, None]:
                last_data = None
                for event in client.ChatCompletions(req):
                    if 'data' in event:
                        try:
                            data = json.loads(event['data'])
                            last_data = data  # Store the last data chunk for search results
                            for choice in data.get('Choices', []):
                                if 'Delta' in choice and 'Content' in choice['Delta']:
                                    yield choice['Delta']['Content']
                        except json.JSONDecodeError:
                            continue
                
                # After the main response, yield search results if available
                if last_data:
                    search_results = self._format_search_results(last_data)
                    if search_results:
                        yield search_results
            
            return stream_response()
            
        except Exception as e:
            raise Exception(f"Tencent Hunyuan API error: {str(e)}")

class LkeapProvider(BaseTencentProvider):
    """Tencent API provider for LKEAP (Deepseek) models"""
    
    def __init__(self):
        super().__init__()
        self._region = "ap-shanghai"  # Default region for LKEAP
        self._model_mapping = {
            "deepseek-r1": "deepseek-r1",
            "deepseek-v3": "deepseek-v3"
        }
        self._supported_regions = ["ap-guangzhou", "ap-shanghai"]
        self._timeout = 300  # 5 minutes timeout

    def _create_chat_request(
        self,
        prompt: str,
        model: str,
        stream: bool = True,
    ) -> lkeap_models.ChatCompletionsRequest:
        """Create a chat request for LKEAP API."""
        if model not in self._model_mapping:
            raise ValueError(f"Unsupported model: {model}. Must be one of: {list(self._model_mapping.keys())}")
            
        req = lkeap_models.ChatCompletionsRequest()
        req.Model = self._model_mapping[model]
        req.Stream = stream
        
        # Create message
        message = lkeap_models.Message()
        message.Role = "user"
        message.Content = prompt
        req.Messages = [message]
        
        return req
        
    async def _stream_response(self, response: AsyncGenerator) -> AsyncGenerator[str, None]:
        """Handle streaming response"""
        saw_reasoning = False
        async for chunk in response:
            if hasattr(chunk.Choices[0], 'Reasoning') and chunk.Choices[0].Reasoning:
                if not saw_reasoning:
                    yield "<think>"
                    saw_reasoning = True
                yield chunk.Choices[0].Reasoning
            elif hasattr(chunk.Choices[0].Message, 'Content') and chunk.Choices[0].Message.Content:
                if saw_reasoning:
                    yield "</think>\n"
                    saw_reasoning = False
                yield chunk.Choices[0].Message.Content

    async def _complete_response(self, response) -> str:
        """Handle non-streaming response"""
        content = []
        if hasattr(response.Choices[0], 'Reasoning') and response.Choices[0].Reasoning:
            content.extend(["<think>", response.Choices[0].Reasoning, "</think>\n"])
        content.append(response.Choices[0].Message.Content)
        return "".join(content)

    async def complete(
        self,
        prompt: str,
        model: str,
        api_key: Dict[str, str],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        image_paths: Optional[List[str]] = None,
        web_search: bool = False,
        **kwargs: Dict[str, Any]
    ) -> Union[str, AsyncGenerator[str, None]]:
        """Complete a prompt using Tencent's LKEAP API"""
        if image_paths:
            raise ValueError("LKEAP API does not support image inputs")

        # Get region from kwargs or use default
        region = kwargs.get('region', self._region)
        if region not in self._supported_regions:
            raise ValueError(f"LKEAP API only supports the following regions: {', '.join(self._supported_regions)}")
            
        try:
            # Initialize client with longer timeout
            cred = self._get_credentials(api_key)
            http_profile = HttpProfile()
            http_profile.reqTimeout = self._timeout
            client_profile = ClientProfile()
            client_profile.httpProfile = http_profile
            
            client = lkeap_client.LkeapClient(cred, region, client_profile)
            
            # Create request
            req = self._create_chat_request(
                prompt=prompt,
                model=model,
                stream=True if isinstance(prompt, AsyncGenerator) else False
            )
            
            # Send request
            response = client.ChatCompletions(req)
            
            if isinstance(response, AsyncGenerator):
                return self._stream_response(response)
            else:
                return await self._complete_response(response)
                
        except Exception as e:
            raise Exception(f"Error completing prompt with LKEAP: {str(e)}")