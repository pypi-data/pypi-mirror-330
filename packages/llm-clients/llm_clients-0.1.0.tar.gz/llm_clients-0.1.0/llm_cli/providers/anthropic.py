"""
Anthropic provider implementation for Claude models

This module implements the Provider interface for Anthropic's Claude models.
It supports both streaming and non-streaming completions using the official
Anthropic Python client.

"""
from typing import Optional, Union, AsyncGenerator, Dict, Any, List
import anthropic
import base64
from anthropic.types import MessageParam

from llm_cli.providers.base import Provider, register_provider

@register_provider("anthropic")
class AnthropicProvider(Provider):
    """Anthropic API provider for Claude models
    
    This provider implements the completion interface using Anthropic's
    official Python client. It supports both streaming and non-streaming
    responses, with streaming being the default for better user experience.
    
    The provider automatically handles API errors and provides detailed
    error messages for debugging.
    """
    
    # Supported parameters for Anthropic API
    SUPPORTED_PARAMS = {
        "model",
        "messages",
        "max_tokens",
        "temperature",
        "system",
        "stream",
        "metadata",
        "stop_sequences",
        "top_p",
        "top_k",
    }
    
    def __init__(self):
        """Initialize the provider"""
        self._system_prompt = "You are Claude, a helpful AI assistant."
    
    async def complete(
        self,
        prompt: str,
        model: str,
        api_key: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        system: Optional[str] = None,
        image_paths: Optional[List[str]] = None,
        image_detail: str = "auto",
        **kwargs: Dict[str, Any]
    ) -> Union[str, AsyncGenerator[str, None]]:
        """Complete a prompt using the Anthropic API
        
        Args:
            prompt: The prompt to complete
            model: Anthropic model to use (e.g. "claude-3-opus-20240229")
            api_key: Anthropic API key
            temperature: Sampling temperature (default: 0.7)
            max_tokens: Maximum tokens to generate (optional)
            system: System prompt to override default (optional)
            image_paths: List of paths to image files (optional)
            image_detail: Image detail level (auto, low, high) (optional)
            **kwargs: Additional parameters to pass to the Anthropic API
        
        Returns:
            Either a complete response string or an async generator yielding
            response chunks when streaming is enabled (default).
            
        Raises:
            Exception: If the API request fails or returns an error
        """
        # Initialize client
        try:
            client = anthropic.Anthropic(api_key=api_key)
        except Exception as e:
            raise Exception(f"Failed to initialize Anthropic client: {str(e)}")
        
        # Prepare message content
        content: List[Union[str, Dict[str, Any]]] = []
        
        # Add images if provided
        if image_paths:
            for image_path in image_paths:
                try:
                    with open(image_path, "rb") as f:
                        image_data = base64.b64encode(f.read()).decode("utf-8")
                    content.append({
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": image_data
                        }
                    })
                except Exception as e:
                    raise Exception(f"Failed to process image {image_path}: {str(e)}")
        
        # Add text content
        content.append({"type": "text", "text": prompt})
        
        # Prepare parameters
        params = {
            "model": model,
            "max_tokens": max_tokens or 1024,  # Anthropic requires max_tokens
            "messages": [{"role": "user", "content": content}],
            "temperature": temperature,
            "system": system or self._system_prompt,
        }
            
        # Add any additional supported parameters
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in self.SUPPORTED_PARAMS}
        params.update(filtered_kwargs)

        try:
            # Create streaming response
            stream = client.messages.stream(**params)
            return self._stream_response(stream)
        except anthropic.APIError as e:
            # Handle specific API errors
            error_msg = f"Anthropic API error ({e.status_code}): {e.message}"
            if e.status_code == 401:
                error_msg = "Invalid API key. Please check your credentials."
            elif e.status_code == 400:
                error_msg = f"Invalid request: {e.message}"
            raise Exception(error_msg) from e
        except Exception as e:
            # If streaming fails, try non-streaming
            try:
                return await self._complete_response(client, params)
            except Exception as e2:
                raise Exception(f"Both streaming and non-streaming requests failed: {str(e2)}") from e2

    async def _stream_response(self, stream) -> AsyncGenerator[str, None]:
        """Handle streaming response from Anthropic API
        
        Args:
            stream: Anthropic stream response object
            
        Yields:
            Text chunks from the response stream
            
        Raises:
            Exception: If there is an error processing the stream
        """
        try:
            with stream as response:
                for text in response.text_stream:
                    yield text
        except Exception as e:
            raise Exception(f"Error processing Anthropic stream: {str(e)}")

    async def _complete_response(self, client: anthropic.Anthropic, params: dict) -> str:
        """Handle non-streaming response from Anthropic API
        
        Args:
            client: Initialized Anthropic client
            params: Parameters for the completion request
            
        Returns:
            Complete response text
            
        Raises:
            Exception: If there is an error getting the response
        """
        try:
            # Disable streaming for complete response
            params["stream"] = False
            response = client.messages.create(**params)
            return response.content[0].text
        except anthropic.APIError as e:
            error_msg = f"Anthropic API error ({e.status_code}): {e.message}"
            if e.status_code == 401:
                error_msg = "Invalid API key. Please check your credentials."
            elif e.status_code == 400:
                error_msg = f"Invalid request: {e.message}"
            raise Exception(error_msg) from e
        except Exception as e:
            raise Exception(f"Failed to get complete response: {str(e)}")

# Ensure the provider is registered
provider = AnthropicProvider()
