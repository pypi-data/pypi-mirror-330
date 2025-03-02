"""
Tools package for llm-cli
"""
import importlib
import pkgutil
import re
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Optional, Callable, Pattern
import xml.etree.ElementTree as ET
import logging
import asyncio

logger = logging.getLogger(__name__)

class Tool(ABC):
    """Base class for all tools"""
    
    def __init__(self):
        """Initialize tool with empty XML tag handlers"""
        self._xml_handlers: Dict[str, Callable[[ET.Element], str]] = {}
        self._xml_patterns: Dict[str, Pattern] = {}
        self.verbose = False  # Initialize verbose flag
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the tool"""
        pass
        
    @property
    @abstractmethod
    def description(self) -> str:
        """Description of what the tool does"""
        pass
        
    @abstractmethod
    async def generate_prompt(self, input: str, **kwargs) -> str:
        """Generate a prompt for the tool"""
        pass
    
    def register_xml_tag(self, tag_name: str, handler: Callable[[ET.Element], str]):
        """Register an XML tag handler for this tool
        
        Args:
            tag_name: Name of the XML tag to handle (e.g. 'read_file')
            handler: Function that takes an ElementTree.Element and returns a string response
        """
        self._xml_handlers[tag_name] = handler
        # Create regex pattern that matches the entire tag including content
        # Match <tag>content</tag> where content doesn't contain the tag name
        self._xml_patterns[tag_name] = re.compile(
            f'<{tag_name}>((?:(?!</?{tag_name}).)*)</{tag_name}>', 
            re.DOTALL
        )
    
    async def _handle_xml_tag(self, tag_name: str, match: re.Match) -> str:
        """Handle a matched XML tag using its registered handler
        
        Args:
            tag_name: The name of the XML tag
            match: The regex match object containing the full tag
            
        Returns:
            The handler's response string
        """
        try:
            # Get content from first capture group with simpler pattern
            content = match.group(1)
            logger.debug(f"Processing {tag_name} tag with content: {content}")
            
            # Create XML with proper escaping
            xml = f"<{tag_name}>{content}</{tag_name}>"
            
            # Parse the XML
            root = ET.fromstring(xml)
            
            # Call the registered handler
            handler = self._xml_handlers[tag_name]
            logger.debug(f"Calling handler for {tag_name}")
            
            # Handle both async and sync handlers
            if asyncio.iscoroutinefunction(handler):
                result = await handler(root)
            else:
                result = handler(root)
                
            if self.verbose:
                logger.debug(f"{tag_name}: {content} -> {result}")
            return str(result) if result is not None else ""
            
        except ET.ParseError as e:
            logger.error(f"XML parse error in {tag_name} tag: {e}")
            return f"Error: Invalid XML format in {tag_name} tag - {str(e)}"
        except Exception as e:
            logger.error(f"Error processing {tag_name} tag: {e}")
            return f"Error processing {tag_name} tag: {str(e)}"
        
    async def execute(self, input: str, verbose: bool = False, **kwargs) -> str:
        """Execute the tool's operation by processing all registered XML tags
        
        This base implementation processes all registered XML tags in the input.
        Subclasses can override this to add additional processing if needed.
        """
        self.verbose = verbose  # Set verbose flag from execute call
        result = input
        
        logger.debug(f"Executing tool with input: {input}")
        logger.debug(f"Registered patterns: {list(self._xml_patterns.keys())}")
        
        # Process each registered tag
        for tag_name, pattern in self._xml_patterns.items():
            logger.debug(f"Looking for {tag_name} tags with pattern: {pattern.pattern}")
            matches = list(pattern.finditer(result))
            if matches:
                logger.debug(f"Found {len(matches)} {tag_name} tags")
                for match in matches:
                    logger.debug(f"Match found: {match.group(0)}")
                    replacement = await self._handle_xml_tag(tag_name, match)
                    result = result.replace(match.group(0), replacement)
            else:
                logger.debug(f"No {tag_name} tags found")
            
        return result

class ToolRegistry:
    """Registry for available tools"""
    def __init__(self):
        self._tools: Dict[str, Tool] = {}
        
    def register(self, tool: Tool):
        """Register a tool"""
        self._tools[tool.name] = tool
        
    def get_tool(self, name: str) -> Optional[Tool]:
        """Get a tool by name"""
        return self._tools.get(name)
        
    def list_tools(self) -> List[Dict[str, str]]:
        """List all registered tools"""
        return [{"name": tool.name, "description": tool.description} 
                for tool in self._tools.values()]

# Global registry instance
registry = ToolRegistry()

# Automatically import all modules in the tools package
package_dir = Path(__file__).resolve().parent
for (_, module_name, _) in pkgutil.iter_modules([str(package_dir)]):
    # Skip importing this module
    if module_name != '__init__':
        importlib.import_module(f"{__package__}.{module_name}")

__all__ = ["Tool", "registry"] 