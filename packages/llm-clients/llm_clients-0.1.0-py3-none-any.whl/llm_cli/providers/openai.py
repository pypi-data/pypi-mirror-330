"""
OpenAI provider implementation
"""
from typing import Optional, Union, AsyncGenerator, List
import json
import aiohttp
import base64
from pathlib import Path

from llm_cli.providers.base import Provider, register_provider

@register_provider("openai")
class OpenAIProvider(Provider):
    """OpenAI API provider"""
    
    async def complete(
        self,
        prompt: str,
        model: str,
        api_key: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        image_paths: Optional[List[str]] = None,
        image_detail: str = "auto",
        **kwargs
    ) -> Union[str, AsyncGenerator[str, None]]:
        """Complete a prompt using the OpenAI API"""
        # API endpoint
        url = "https://api.openai.com/v1/chat/completions"
        
        # Prepare headers
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Prepare messages with image content if provided
        messages = []
        if image_paths:
            # Convert image detail to OpenAI's format
            detail_map = {
                "low": "low",
                "high": "high",
                "auto": "auto"
            }
            
            # Prepare content array with images
            content = []
            for image_path in image_paths:
                # Read and encode image
                with open(image_path, "rb") as f:
                    image_data = base64.b64encode(f.read()).decode("utf-8")
                
                content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_data}",
                        "detail": detail_map.get(image_detail, "auto")
                    }
                })
            
            # Add text content
            content.append({
                "type": "text",
                "text": prompt
            })
            
            messages.append({"role": "user", "content": content})
        else:
            messages.append({"role": "user", "content": prompt})
        
        # Prepare parameters
        params = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "stream": True  # Always try streaming first
        }
        if max_tokens is not None:
            params["max_tokens"] = max_tokens
            
        # Add any additional parameters
        params.update(kwargs)

        # Try streaming first
        try:
            return self._stream_response(url, headers, params)
        except Exception as e:
            # Fall back to non-streaming if streaming fails
            return await self._complete_response(url, headers, {**params, "stream": False})

    async def _stream_response(self, url: str, headers: dict, params: dict) -> AsyncGenerator[str, None]:
        """Handle streaming response"""
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
            raise Exception(f"OpenAI API streaming error: {str(e)}")

    async def _complete_response(self, url: str, headers: dict, params: dict) -> str:
        """Handle non-streaming response"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=params) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise Exception(f"API returned status {response.status}: {error_text}")
                    
                    data = await response.json()
                    return data["choices"][0]["message"]["content"].strip()
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")

# Ensure the provider is registered
provider = OpenAIProvider() 
