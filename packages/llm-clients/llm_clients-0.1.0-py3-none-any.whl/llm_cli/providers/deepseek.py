"""
Deepseek provider implementation
"""
from typing import Optional, Union, AsyncGenerator, List, Dict, Any
import json
from openai import OpenAI, AsyncOpenAI

from llm_cli.providers.base import Provider, register_provider

DEEPSEEK_MODELS = ["deepseek-chat", "deepseek-reasoner"]

@register_provider("deepseek")
class DeepseekProvider(Provider):
    """Deepseek API provider"""
    
    async def complete(
        self,
        prompt: str,
        model: str,
        api_key: str,
        **kwargs
    ) -> Union[str, AsyncGenerator[str, None]]:
        """Complete a prompt using the Deepseek API
        
        Args:
            prompt: The user's input prompt
            model: Model to use (deepseek-chat or deepseek-reasoner)
            api_key: Deepseek API key
            **kwargs: Additional parameters including:
                temperature: Sampling temperature (0-2)
                max_tokens: Maximum tokens to generate
                presence_penalty: Number between -2.0 and 2.0
                frequency_penalty: Number between -2.0 and 2.0
                response_format: Optional format specification {"type": "text"} or {"type": "json_object"}
                system_message: Optional system message to set context
        """
        if model not in DEEPSEEK_MODELS:
            raise ValueError(f"Model must be one of {DEEPSEEK_MODELS}")
            
        # Initialize OpenAI client
        client = AsyncOpenAI(api_key=api_key, base_url="https://api.deepseek.com/v1")
        
        # Prepare messages
        messages = []
        if system_message := kwargs.get('system_message'):
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": prompt})
        
        # Prepare parameters
        params = {
            "model": model,
            "messages": messages,
            "stream": True  # Always try streaming first
        }
        
        # Add optional parameters
        for key in ['temperature', 'max_tokens', 'presence_penalty', 'frequency_penalty', 'response_format']:
            if key in kwargs:
                params[key] = kwargs[key]
            
        # Try streaming first
        try:
            return self._stream_response(client, params)
        except Exception as e:
            # Fall back to non-streaming if streaming fails
            return await self._complete_response(client, {**params, "stream": False})

    async def _stream_response(self, client: AsyncOpenAI, params: dict) -> AsyncGenerator[str, None]:
        """Handle streaming response"""
        try:
            response = await client.chat.completions.create(**params)
            reasoning_content = ""
            has_yielded_reasoning = False
            
            async for chunk in response:
                delta = chunk.choices[0].delta
                if hasattr(delta, 'reasoning_content') and delta.reasoning_content:
                    reasoning_content += delta.reasoning_content
                elif delta.content:
                    # Once we start getting content, yield any accumulated reasoning first
                    if reasoning_content and not has_yielded_reasoning:
                        yield f"<think>{reasoning_content}</think>"
                        has_yielded_reasoning = True
                    yield delta.content
            
            # If we have reasoning content but never got any content chunks, yield it now
            if reasoning_content and not has_yielded_reasoning:
                yield f"<think>{reasoning_content}</think>"
                    
        except Exception as e:
            raise Exception(f"Deepseek API streaming error: {str(e)}")

    async def _complete_response(self, client: AsyncOpenAI, params: dict) -> str:
        """Handle non-streaming response"""
        try:
            response = await client.chat.completions.create(**params)
            result = ""
            message = response.choices[0].message
            
            if hasattr(message, 'reasoning_content') and message.reasoning_content:
                result += f"<think>{message.reasoning_content}</think>"
            
            result += message.content.strip()
            return result
        except Exception as e:
            raise Exception(f"Deepseek API error: {str(e)}")

# Ensure the provider is registered
provider = DeepseekProvider()

