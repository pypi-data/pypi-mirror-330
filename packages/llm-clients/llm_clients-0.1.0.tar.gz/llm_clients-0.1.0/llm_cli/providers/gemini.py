"""
Gemini provider implementation for Google's Gemini models

This module implements the Provider interface for Google's Gemini models.
It supports both streaming and non-streaming completions, as well as image inputs.
"""
from typing import Optional, Union, AsyncGenerator, Dict, Any, List
import os
import mimetypes
from google import genai
from google.genai import types
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch

from llm_cli.providers.base import Provider, register_provider

@register_provider("gemini")
class GeminiProvider(Provider):
    """Google Gemini API provider"""
    
    def __init__(self):
        """Initialize the provider"""
        self._default_config = {
            'temperature': 0.7,
            'top_p': 0.95,
            'top_k': 20,
            'max_output_tokens': 16384,
        }

    def _get_mime_type(self, file_path: str) -> str:
        """Get MIME type for a file."""
        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type or not mime_type.startswith('image/'):
            return 'image/jpeg'  # Default to JPEG
        return mime_type

    def _load_image(self, image_path: str) -> tuple[bytes, str]:
        """Load image file as bytes."""
        with open(image_path, 'rb') as f:
            return f.read(), self._get_mime_type(image_path)

    def _create_content_parts(self, prompt: str, image_paths: Optional[List[str]] = None) -> List[types.Content]:
        """Create content parts for the request."""
        parts = []
        
        # Add text prompt
        text_part = types.Content(
            role='user',
            parts=[types.Part(text=prompt)]
        )
        parts.append(text_part)
        
        # Add images if provided
        if image_paths:
            for img_path in image_paths:
                img_bytes, mime_type = self._load_image(img_path)
                image_part = types.Content(
                    role='user',
                    parts=[types.Part(
                        inline_data={
                            'mime_type': mime_type,
                            'data': img_bytes
                        }
                    )]
                )
                parts.append(image_part)
        
        return parts
    
    async def complete(
        self,
        prompt: str,
        model: str,
        api_key: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        image_paths: Optional[List[str]] = None,
        web_search: bool = False,
        **kwargs: Dict[str, Any]
    ) -> Union[str, AsyncGenerator[str, None]]:
        """Complete a prompt using the Gemini API
        
        Args:
            prompt: The prompt to complete
            model: Gemini model to use (e.g. "gemini-2.0-flash-exp")
            api_key: Gemini API key
            temperature: Sampling temperature (default: 0.7)
            max_tokens: Maximum tokens to generate (optional)
            image_paths: List of paths to image files (optional)
            web_search: Enable web search/grounding (optional)
            **kwargs: Additional parameters to pass to the Gemini API
            
        Returns:
            Either a complete response string or an async generator yielding
            response chunks when streaming is enabled (default).
            
        Raises:
            Exception: If the API request fails or returns an error
        """
        try:
            # Initialize client
            client = genai.Client(api_key=api_key)
            
            # Prepare generation config
            config = self._default_config.copy()
            config.update({
                'temperature': temperature,
                'max_output_tokens': max_tokens or config['max_output_tokens']
            })
            
            # Add web search tool if enabled
            tools = []
            if web_search:
                tools.append(Tool(google_search=GoogleSearch()))
                
            generate_config = GenerateContentConfig(
                **config,
                tools=tools if tools else None,
                response_modalities=["TEXT"]
            )
            
            # Create content parts with text and images
            contents = self._create_content_parts(prompt, image_paths)
            
            # If using images or web search, we can't stream
            if image_paths or web_search:
                response = client.models.generate_content(
                    model=model,
                    contents=contents,
                    config=generate_config
                )
                
                # Include grounding metadata if web search was used
                if web_search and response.candidates[0].grounding_metadata:
                    search_results = response.candidates[0].grounding_metadata.search_entry_point.rendered_content
                    return f"{response.text}\n\nSearch Results:\n{search_results}"
                return response.text
            
            # For text-only without web search, try streaming first
            try:
                stream = client.models.generate_content_stream(
                    model=model,
                    contents=contents,
                    config=generate_config
                )
                return self._stream_response(stream)
            except Exception:
                # Fall back to non-streaming
                response = client.models.generate_content(
                    model=model,
                    contents=contents,
                    config=generate_config
                )
                return response.text
                
        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")
    
    async def _stream_response(self, stream) -> AsyncGenerator[str, None]:
        """Handle streaming response from Gemini API"""
        try:
            for chunk in stream:
                if chunk.text:
                    yield chunk.text
        except Exception as e:
            raise Exception(f"Error processing Gemini stream: {str(e)}")

# Ensure the provider is registered
provider = GeminiProvider() 
