"""
Decorators for tool registration
"""
from typing import Type, TypeVar

from llm_cli.tools import Tool, registry

T = TypeVar('T', bound=Tool)

def register_tool(cls: Type[T]) -> Type[T]:
    """
    Decorator to automatically register a tool class.
    
    Example:
        @register_tool
        class MyTool(Tool):
            ...
    """
    # Create an instance and register it
    instance = cls()
    registry.register(instance)
    return cls 