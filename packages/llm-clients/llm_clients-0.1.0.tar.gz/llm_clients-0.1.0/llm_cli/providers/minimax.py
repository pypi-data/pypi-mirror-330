"""
Minimax provider implementation
"""
from typing import Optional, Union, AsyncGenerator, List, Dict, Any
import json
import aiohttp
import base64
from enum import Enum
from pathlib import Path

from llm_cli.providers.base import Provider, register_provider

class MinimaxModel(str, Enum):
    """Available Minimax models"""
    CHAT = "abab6.5s-chat"
    TEXT = "MiniMax-Text-01"

@register_provider("minimax")
class MinimaxProvider(Provider):
    """Minimax API provider"""
    
    async def complete(
        self,
        prompt: str,
        model: str,
        api_key: str,
        **kwargs
    ) -> Union[str, AsyncGenerator[str, None]]:
        """Complete a prompt using the Minimax API
        
        Args:
            prompt: The user's input prompt
            model: Model to use (defaults to abab6.5s-chat)
            api_key: Minimax API key
            **kwargs: Additional parameters including:
                temperature: Sampling temperature
                max_tokens: Maximum tokens to generate
                top_p: Top p sampling parameter
                system_message: Optional system message to set context
                image_paths: Optional list of image paths for image input
        """
        # API endpoint
        base_url = "https://api.minimax.chat/v1"
        url = f"{base_url}/text/chatcompletion_v2"
        
        # Prepare headers
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Prepare messages
        messages = []
        if system_message := kwargs.get('system_message'):
            messages.append({"role": "system", "content": system_message})
            
        # Handle image input if provided
        image_paths = kwargs.get('image_paths', [])
        if image_paths:
            # For image input, we need to prepare the content differently
            content = []
            content.append({"type": "text", "text": prompt})
            
            for image_path in image_paths:
                try:
                    with open(image_path, "rb") as image_file:
                        base64_image = base64.b64encode(image_file.read()).decode('utf-8')
                        content.append({
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                        })
                except Exception as e:
                    raise Exception(f"Error reading image file {image_path}: {e}")
            
            messages.append({"role": "user", "content": content})
        else:
            # For text-only input
            messages.append({"role": "user", "content": prompt})
        
        # Prepare parameters
        params = {
            "model": model,
            "messages": messages,
            "stream": True,
            "temperature": kwargs.get('temperature', 0.7),
            "top_p": kwargs.get('top_p', 0.95),
        }
        
        if max_tokens := kwargs.get('max_tokens'):
            params["max_tokens"] = max_tokens
            
        # Try streaming first
        try:
            return self._stream_response(url, headers, params)
        except Exception as e:
            # Fall back to non-streaming if streaming fails
            return await self._complete_response(url, headers, {**params, "stream": False})

    async def _stream_response(self, url: str, headers: dict, params: dict) -> AsyncGenerator[str, None]:
        """Handle streaming response"""
        buffer = ""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=params) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise Exception(f"API returned status {response.status}: {error_text}")
                    
                    async for chunk in response.content.iter_chunked(8192):
                        buffer += chunk.decode('utf-8')
                        while '\n' in buffer:
                            line, buffer = buffer.split('\n', 1)
                            line = line.strip()
                            if not line.startswith("data:"):
                                continue
                            
                            try:
                                data = json.loads(line.strip("data:"))
                                if data and "choices" in data and data["choices"]:
                                    delta = data["choices"][0].get("delta", {})
                                    if delta.get("role") == "assistant" and delta.get("content"):
                                        yield delta["content"]
                            except json.JSONDecodeError:
                                continue
                                
            # Handle remaining buffer
            if buffer and buffer.startswith("data:"):
                try:
                    data = json.loads(buffer.strip("data:"))
                    if data and "choices" in data and data["choices"]:
                        delta = data["choices"][0].get("delta", {})
                        if delta.get("role") == "assistant" and delta.get("content"):
                            yield delta["content"]
                except json.JSONDecodeError:
                    pass  # Ignore invalid JSON in remaining buffer
                    
        except Exception as e:
            raise Exception(f"Minimax API streaming error: {str(e)}")

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
            raise Exception(f"Minimax API error: {str(e)}")

# Ensure the provider is registered
provider = MinimaxProvider()

