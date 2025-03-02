"""
SiliconFlow provider implementation

This module implements the Provider interface for SiliconFlow's LLM models.
It uses SiliconFlow's OpenAI-compatible API endpoint.
"""
from typing import Optional, Union, AsyncGenerator, Dict, Any, List
import aiohttp
import json
import base64
from pathlib import Path

from llm_cli.providers.base import Provider, register_provider

@register_provider("siliconflow")
class SiliconFlowProvider(Provider):
    """SiliconFlow API provider"""
    
    def __init__(self):
        """Initialize the provider"""
        self._api_base = "https://api.siliconflow.cn/v1"
        self._api_endpoint = f"{self._api_base}/chat/completions"
    
    async def complete(
        self,
        prompt: str,
        model: str,
        api_key: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        image_paths: Optional[List[str]] = None,
        image_detail: str = "high",
        **kwargs: Dict[str, Any]
    ) -> Union[str, AsyncGenerator[str, None]]:
        """Complete a prompt using the SiliconFlow API
        
        Args:
            prompt: The prompt to complete
            model: Model to use (e.g. 'deepseek-ai/DeepSeek-V2.5')
            api_key: SiliconFlow API key
            temperature: Sampling temperature (default: 0.7)
            max_tokens: Maximum tokens to generate (optional)
            image_paths: List of paths to image files (optional)
            image_detail: Image detail level, one of "low", "high", "auto" (default: "high")
            **kwargs: Additional parameters to pass to the API
        
        Returns:
            Either a complete response string or an async generator yielding
            response chunks when streaming is enabled (default).
            
        Raises:
            Exception: If the API request fails or returns an error
        """
        # Prepare headers
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Prepare message content
        content = []
        
        # Add images if provided
        if image_paths:
            for img_path in image_paths:
                try:
                    # Read and encode image
                    with open(img_path, "rb") as f:
                        img_data = f.read()
                        img_base64 = base64.b64encode(img_data).decode()
                    
                    # Add image content
                    content.append({
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{img_base64}",
                            "detail": image_detail
                        }
                    })
                except Exception as e:
                    raise Exception(f"Failed to process image {img_path}: {str(e)}")
        
        # Add text prompt
        content.append({
            "type": "text",
            "text": prompt
        })
        
        # Prepare parameters
        params = {
            "model": model,
            "messages": [{
                "role": "user",
                "content": content if image_paths else prompt
            }],
            "temperature": temperature,
            "stream": True  # Always use streaming for better UX
        }
        if max_tokens is not None:
            params["max_tokens"] = max_tokens
            
        # Add any additional parameters
        params.update(kwargs)

        try:
            # Create streaming response
            return self._stream_response(self._api_endpoint, headers, params)
        except Exception as e:
            # If streaming fails, try non-streaming
            try:
                return await self._complete_response(self._api_endpoint, headers, {**params, "stream": False})
            except Exception as e2:
                raise Exception(f"Both streaming and non-streaming requests failed: {str(e2)}") from e2

    async def _stream_response(self, url: str, headers: dict, params: dict) -> AsyncGenerator[str, None]:
        """Handle streaming response from SiliconFlow API
        
        Args:
            url: API endpoint URL
            headers: Request headers
            params: Request parameters
            
        Yields:
            Text chunks from the response stream
            
        Raises:
            Exception: If there is an error processing the stream
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=params) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise Exception(f"API returned status {response.status}: {error_text}")
                    
                    async for line in response.content:
                        line = line.decode('utf-8').strip()
                        if line:
                            if line.startswith('data: '):
                                line = line[6:]  # Remove 'data: ' prefix
                            if line == '[DONE]':
                                break
                            try:
                                data = json.loads(line)
                                if content := data.get('choices', [{}])[0].get('delta', {}).get('content'):
                                    yield content
                            except json.JSONDecodeError:
                                continue
        except Exception as e:
            raise Exception(f"Error processing SiliconFlow stream: {str(e)}")

    async def _complete_response(self, url: str, headers: dict, params: dict) -> str:
        """Handle non-streaming response from SiliconFlow API
        
        Args:
            url: API endpoint URL
            headers: Request headers
            params: Request parameters
            
        Returns:
            Complete response text
            
        Raises:
            Exception: If there is an error getting the response
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=params) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise Exception(f"API returned status {response.status}: {error_text}")
                    
                    data = await response.json()
                    return data["choices"][0]["message"]["content"].strip()
        except Exception as e:
            raise Exception(f"Failed to get complete response: {str(e)}")

# Ensure the provider is registered
provider = SiliconFlowProvider()
