"""
SambaNova provider implementation
"""
from typing import Optional, Union, AsyncGenerator
import json
import aiohttp

from llm_cli.providers.base import Provider, register_provider

@register_provider("sambanova")
class SambanovaProvider(Provider):
    """SambaNova API provider"""
    
    async def complete(
        self,
        prompt: str,
        model: str,
        api_key: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = True,
        **kwargs
    ) -> Union[str, AsyncGenerator[str, None]]:
        """Complete a prompt using the SambaNova API"""
        # API endpoint
        url = "https://api.sambanova.ai/v1/chat/completions"
        
        # Prepare headers
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Prepare parameters
        params = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "stream": stream
        }
        if max_tokens is not None:
            params["max_tokens"] = max_tokens
            
        # Add any additional parameters
        params.update(kwargs)

        async def stream_response() -> AsyncGenerator[str, None]:
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
                raise Exception(f"SambaNova API streaming error: {str(e)}")

        # Return streaming generator if streaming is enabled
        if stream:
            return stream_response()
            
        # Otherwise return complete response
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=params) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise Exception(f"API returned status {response.status}: {error_text}")
                    
                    data = await response.json()
                    return data["choices"][0]["message"]["content"].strip()
        except Exception as e:
            raise Exception(f"SambaNova API error: {str(e)}")

# Ensure the provider is registered
provider = SambanovaProvider() 