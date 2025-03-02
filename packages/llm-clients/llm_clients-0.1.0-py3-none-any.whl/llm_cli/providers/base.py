"""
Base classes for LLM providers
"""
from abc import ABC, abstractmethod
from typing import Dict, Optional, Type, AsyncGenerator, Union

# Provider registry
_PROVIDERS: Dict[str, Type["Provider"]] = {}

def register_provider(name: str):
    """Decorator to register a provider"""
    def decorator(cls: Type["Provider"]) -> Type["Provider"]:
        _PROVIDERS[name] = cls
        return cls
    return decorator

def get_provider(name: str) -> Optional["Provider"]:
    """Get a provider instance by name"""
    provider_class = _PROVIDERS.get(name)
    if provider_class:
        return provider_class()
    return None

class Provider(ABC):
    """Base class for LLM providers"""
    
    @abstractmethod
    async def complete(
        self,
        prompt: str,
        model: str,
        api_key: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> Union[str, AsyncGenerator[str, None]]:
        """Complete a prompt using the provider's API
        
        Args:
            prompt: The prompt to complete
            model: Model to use
            api_key: API key for authentication
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional provider-specific parameters
            
        Returns:
            Either a complete response string or an async generator yielding response chunks,
            depending on the provider's capabilities and optimal delivery method
        """
        raise NotImplementedError() 