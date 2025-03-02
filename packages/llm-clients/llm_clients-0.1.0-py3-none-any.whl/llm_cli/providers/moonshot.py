"""
Moonshot provider implementation for Moonshot AI's models

This module implements the Provider interface for Moonshot AI's models.
It supports streaming completions, vision capabilities, and web search functionality.
"""
from typing import Optional, Union, AsyncGenerator, List, Dict, Any
import json
import aiohttp
import base64
import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

from llm_cli.providers.base import Provider, register_provider

@register_provider("moonshot")
class MoonshotProvider(Provider):
    """Moonshot AI API provider"""
    
    def __init__(self):
        """Initialize the provider with default web search tool"""
        self._default_tools = [
            {
                "type": "builtin_function",
                "function": {
                    "name": "$web_search",
                },
            }
        ]
    
    def _prepare_image_content(self, image_paths: List[str], image_detail: str = "high") -> List[Dict[str, Any]]:
        """Prepare image content for the API request"""
        content = []
        for image_path in image_paths:
            with open(image_path, "rb") as f:
                image_data = f.read()
            # Get file extension and create base64 image URL
            ext = os.path.splitext(image_path)[1].lstrip('.')
            if not ext:
                ext = 'jpeg'  # Default to jpeg if no extension
            image_url = f"data:image/{ext};base64,{base64.b64encode(image_data).decode('utf-8')}"
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": image_url,
                    "detail": image_detail  # Add image detail level
                }
            })
        return content

    async def complete(
        self,
        prompt: str,
        model: str,
        api_key: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        image_paths: Optional[List[str]] = None,
        image_detail: str = "high",
        web_search: bool = False,
        system_prompt: Optional[str] = None,
        messages: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> Union[str, AsyncGenerator[str, None]]:
        """Complete a prompt using the Moonshot AI API
        
        Args:
            prompt: The prompt to complete
            model: Model to use (e.g. "moonshot-v1-8k", "moonshot-v1-32k", "moonshot-v1-128k")
            api_key: API key
            temperature: Sampling temperature (default: 0.7)
            max_tokens: Maximum tokens to generate (optional)
            image_paths: List of paths to image files (optional)
            image_detail: Image detail level, one of "low", "high", "auto" (default: "high")
            web_search: Whether to enable web search capability
            system_prompt: Optional system prompt to set context
            messages: Optional list of previous messages for conversation history
            **kwargs: Additional parameters to pass to the API
        """
        # API endpoint
        url = "https://api.moonshot.cn/v1/chat/completions"
        
        # Prepare headers
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Prepare messages
        if messages is None:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
        
        # Handle image content if provided
        if image_paths:
            content = self._prepare_image_content(image_paths, image_detail)
            content.append({
                "type": "text",
                "text": prompt
            })
            messages.append({"role": "user", "content": content})
        else:
            messages.append({"role": "user", "content": prompt})
        
        # Prepare request parameters
        params = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "stream": True  # Default to streaming
        }
        
        if max_tokens is not None:
            params["max_tokens"] = max_tokens
            
        # Add web search tool if enabled
        if web_search:
            params["tools"] = self._default_tools
            
        # Handle any additional parameters
        for key, value in kwargs.items():
            if value is not None:
                params[key] = value

        # If web search is enabled, we need to handle the complete conversation flow
        if web_search:
            async def search_and_respond():
                tool_call_id = None
                async for chunk in self._stream_response(url, headers, params):
                    if isinstance(chunk, dict):
                        # This is a tool call response
                        if chunk.get('type') == 'tool_call':
                            tool_call_id = chunk['id']
                            # Add tool call to messages
                            messages.append({
                                "role": "assistant",
                                "content": None,
                                "tool_calls": [{
                                    "id": tool_call_id,
                                    "type": "function",
                                    "function": {
                                        "name": "$web_search",
                                        "arguments": json.dumps(chunk['arguments'])
                                    }
                                }]
                            })
                            # Add tool result to messages
                            messages.append({
                                "role": "tool",
                                "tool_call_id": tool_call_id,
                                "name": "$web_search",
                                "content": json.dumps(chunk['arguments'])
                            })
                            # Make second request with updated messages
                            params["messages"] = messages
                            async for content in self._stream_response(url, headers, params):
                                if isinstance(content, str):
                                    yield content
                    elif isinstance(chunk, str):
                        yield chunk
            
            return search_and_respond()
        else:
            # Use streaming by default for non-web-search requests
            if kwargs.get("stream", True):
                return self._stream_response(url, headers, params)
            else:
                return await self._complete_response(url, headers, params)

    async def _stream_response(self, url: str, headers: dict, params: dict) -> AsyncGenerator[Union[str, dict], None]:
        """Handle streaming response in SSE format"""
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=params) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Error from API: {error_text}")

                # Process SSE response line by line
                buffer = ""
                tool_call_buffer = None
                async for line in response.content:
                    line = line.decode('utf-8')
                    if not line.strip():
                        # Empty line indicates end of data block
                        if buffer:
                            if buffer.startswith("data: "):
                                data = buffer[6:].strip()  # Remove "data: " prefix
                                if data == "[DONE]":
                                    break
                                try:
                                    chunk = json.loads(data)
                                    logger.debug(f"Received chunk: {json.dumps(chunk, indent=2)}")
                                    
                                    delta = chunk['choices'][0].get('delta', {})
                                    finish_reason = chunk['choices'][0].get('finish_reason')
                                    logger.debug(f"Delta: {json.dumps(delta, indent=2)}")
                                    logger.debug(f"Finish reason: {finish_reason}")
                                    
                                    # Handle content in delta
                                    if delta.get('content') is not None:
                                        content = delta['content']
                                        if content is not None:  # Don't yield None content
                                            logger.debug(f"Yielding content: {content}")
                                            yield content
                                    
                                    # Handle tool calls
                                    if 'tool_calls' in delta:
                                        tool_calls = delta['tool_calls']
                                        logger.debug(f"Tool calls: {json.dumps(tool_calls, indent=2)}")
                                        for tool_call in tool_calls:
                                            if tool_call_buffer is None:
                                                tool_call_buffer = tool_call
                                            else:
                                                # Merge with existing buffer
                                                if 'function' in tool_call and 'arguments' in tool_call['function']:
                                                    tool_call_buffer['function']['arguments'] += tool_call['function']['arguments']
                                    
                                    # When we get a tool_calls finish reason, yield the complete tool call
                                    if finish_reason == 'tool_calls' and tool_call_buffer:
                                        logger.debug(f"Yielding tool call: {json.dumps(tool_call_buffer, indent=2)}")
                                        yield {
                                            'type': 'tool_call',
                                            'id': tool_call_buffer['id'],
                                            'name': tool_call_buffer['function']['name'],
                                            'arguments': json.loads(tool_call_buffer['function']['arguments'])
                                        }
                                        tool_call_buffer = None
                                        
                                except Exception as e:
                                    logger.error(f"Error processing chunk: {e}")
                                    logger.error(f"Buffer was: {buffer}")
                            buffer = ""
                    else:
                        buffer += line

    async def _complete_response(self, url: str, headers: dict, params: dict) -> str:
        """Handle non-streaming response"""
        params["stream"] = False
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=params) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Error from API: {error_text}")
                
                data = await response.json()
                return data["choices"][0]["message"]["content"]
