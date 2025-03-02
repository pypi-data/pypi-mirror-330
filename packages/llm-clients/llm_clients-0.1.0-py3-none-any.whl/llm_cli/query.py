"""
llm-query: Query LLMs and process responses
"""
import asyncio
import logging
import sys
import warnings
from typing import Optional, Union, AsyncGenerator, List

import click

from llm_cli.providers import get_provider
from llm_cli.config import config  # Import the config instance

# Suppress Pydantic warning about built-in function types
warnings.filterwarnings("ignore", message=".*is not a Python type.*")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(name)s] %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger("query")

async def process_query(
    prompt: str,
    model: str = "default",
    max_tokens: Optional[int] = None,
    web_search: bool = False,
    image_paths: Optional[List[str]] = None,
    image_detail: str = "high",
    verbose: bool = False,
) -> Union[str, AsyncGenerator[str, None]]:
    """Process a query through an LLM provider
    
    Args:
        prompt: Input prompt
        model: Model name or alias
        max_tokens: Max tokens to generate
        web_search: Whether to enable web search (OpenRouter only)
        image_paths: List of paths to image files (optional)
        image_detail: Image detail level, one of "low", "high", "auto" (default: "high")
        verbose: Whether to log details
        
    Returns:
        Either a complete response string or an async generator yielding response chunks
        
    Raises:
        ValueError: If model or provider not found
        Exception: For other errors during processing
    """
    try:
        if verbose:
            logger.info(f"Using model: {model}")
            logger.info("Prompt:")
            logger.info("-" * 40)
            logger.info(prompt)
            logger.info("-" * 40)
            
        # Resolve model to provider and config
        provider_name, model_name, model_config = config.resolve_model(model)
        
        if verbose:
            logger.info(f"Provider: {provider_name}")
            
        # Get provider instance
        provider = get_provider(provider_name)
        if not provider:
            raise ValueError(f"Provider not available: {provider_name}")
            
        # Get API key
        api_key = config.get(f"providers.{provider_name}")
        if not api_key:
            raise ValueError(f"No API key found for provider {provider_name}")
            
        # Prepare parameters
        params = model_config.copy()
        if max_tokens:
            params["max_tokens"] = max_tokens
            
        if web_search:
            params["web_search"] = True
            
        if image_paths:
            params["image_paths"] = image_paths
            params["image_detail"] = image_detail
            
        # Process query through provider
        if verbose:
            logger.info("Querying LLM...")
            
        response = await provider.complete(
            prompt=prompt,
            model=model_name,
            api_key=api_key,
            **params
        )
        
        if verbose:
            if isinstance(response, str):
                logger.info("Raw response content:")
                logger.info("-" * 40)
                logger.info(repr(response))  # Use repr to show raw string content
                logger.info("-" * 40)
            else:
                logger.info("Streaming response...")
                
        return response
        
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise

async def write_response(response: Union[str, AsyncGenerator[str, None]]) -> None:
    """Write response to stdout"""
    if isinstance(response, str):
        if response.strip():  # Only print if there's actual content
            print(response)
    else:
        async for chunk in response:
            if chunk.strip():  # Only print if there's actual content
                print(chunk, end="", flush=True)

@click.command()
@click.argument("text", required=False)
@click.option("--model", "-m", default="default", help="Model to use")
@click.option("--max-tokens", type=int, help="Maximum tokens to generate")
@click.option("--web", is_flag=True, help="Enable web search (OpenRouter only)")
@click.option("--image", multiple=True, help="Path to image file")
@click.option("--image-detail", default="high", type=click.Choice(['low', 'high', 'auto']), help="Image detail level")
@click.option("-v", "--verbose", is_flag=True, help="Show verbose output")
@click.option("--debug", is_flag=True, help="Enable debug logging")
def main(
    text: Optional[str],
    model: str,
    max_tokens: Optional[int],
    web: bool,
    image: List[str],
    image_detail: str,
    verbose: bool,
    debug: bool,
):
    """Process queries through LLM providers.
    
    Input is read from stdin if no text argument is provided.
    Output is always written to stdout.
    
    Examples:\n
        # Query with text \n
        $ llm-query "What is 2+2?" \n
        
        # Query from stdin \n
        $ echo "Calculate 2+2" | llm-query \n
        
        # Show progress \n
        $ echo "What is 2+2?" | llm-query -v \n
        
        # With history from prompt \n
        $ llm-prompt -h chat.log | llm-query \n
    """
    if debug:
        logger.setLevel(logging.DEBUG)
    elif verbose:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.WARNING)
        
    try:
        # Read from stdin if no text argument
        if not text:
            if verbose:
                logger.info("Reading from stdin")
            text = sys.stdin.read().strip()
        
        # Process query
        response = asyncio.run(process_query(
            prompt=text,
            model=model,
            max_tokens=max_tokens,
            web_search=web,
            image_paths=list(image) if image else None,
            image_detail=image_detail,
            verbose=verbose
        ))
        
        # Write response
        if verbose:
            logger.info("Writing response")
        asyncio.run(write_response(response))
            
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()