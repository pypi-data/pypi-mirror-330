"""
Search and replace tool for modifying text files
"""
import json
import logging
import re
from pathlib import Path
from typing import Dict, List, Optional, Union, Tuple

from llm_cli.tools import Tool, registry
from llm_cli.tools.decorators import register_tool

logger = logging.getLogger(__name__)

def validate_operation(op: dict, index: int) -> Tuple[bool, str]:
    """Validate a single search-replace operation"""
    if not isinstance(op, dict):
        return False, f"Operation {index} must be a JSON object"
    if 'search' not in op:
        return False, f"Operation {index} missing 'search' field"
    if 'replace' not in op:
        return False, f"Operation {index} missing 'replace' field"
    if not isinstance(op.get('search'), str):
        return False, f"Operation {index} 'search' must be a string"
    if not isinstance(op.get('replace'), str):
        return False, f"Operation {index} 'replace' must be a string"
    
    # Validate line range if specified
    start_line = op.get('start_line')
    end_line = op.get('end_line')
    if start_line is not None:
        if not isinstance(start_line, int) or start_line < 1:
            return False, f"Operation {index} 'start_line' must be a positive integer"
    if end_line is not None:
        if not isinstance(end_line, int) or end_line < 1:
            return False, f"Operation {index} 'end_line' must be a positive integer"
    if start_line is not None and end_line is not None:
        if start_line > end_line:
            return False, f"Operation {index} 'start_line' cannot be greater than 'end_line'"
    
    return True, ""

def validate_regex_pattern(pattern: str, index: int) -> Tuple[bool, str]:
    """Validate a regex pattern"""
    try:
        re.compile(pattern)
        return True, ""
    except re.error as e:
        return False, f"Operation {index} has invalid regex pattern: {str(e)}"

@register_tool
class SearchReplaceTool(Tool):
    """Tool for search and replace operations"""
    
    def __init__(self):
        """Initialize tool and register XML tag handlers"""
        super().__init__()
        self.register_xml_tag('replace', self._handle_replace)
    
    @property
    def name(self) -> str:
        return "replace"
        
    @property
    def description(self) -> str:
        return "Search and replace text in files"
        
    async def generate_prompt(self, input: str, **kwargs) -> str:
        """Generate a prompt instructing LLM to use search and replace operations"""
        return (
            "You are a tool that generates search and replace operations to modify text files. "
            "You will receive file contents and user requests for modifications.\n\n"
            "You must output search and replace operations in this exact format:\n\n"
            "<replace>\n"
            "<path>file_path_here</path>\n"
            "<operations>[\n"
            "  {\n"
            "    \"search\": \"text to find\",\n"
            "    \"replace\": \"replacement text\",\n"
            "    \"start_line\": null,  # optional: line number to start from\n"
            "    \"end_line\": null,    # optional: line number to end at\n"
            "    \"use_regex\": false,  # optional: whether to use regex\n"
            "    \"ignore_case\": false # optional: whether to ignore case\n"
            "  }\n"
            "]</operations>\n"
            "</replace>\n\n"
            "Important:\n"
            "1. Be precise with search patterns to avoid unintended replacements\n"
            "2. Use regex for complex patterns (set use_regex: true)\n"
            "3. Use line ranges to limit scope when appropriate\n"
            "4. For multi-line replacements, use \\n for newlines\n"
            "5. Consider using line ranges to avoid unintended matches\n\n"
            f"Now please help with this request: {input}"
        )
        
    def _format_error(self, message: str) -> str:
        """Format error response"""
        return (
            "<replace>\n"
            "  <error>\n"
            f"    {message}\n"
            "  </error>\n"
            "</replace>"
        )
        
    async def _handle_replace(self, content: str) -> str:
        """Handle replace operation using simple tag parsing"""
        try:
            # Find path and operations using simple patterns
            path_match = re.search(r'<path>(.*?)</path>', content, re.DOTALL)
            operations_match = re.search(r'<operations>(.*?)</operations>', content, re.DOTALL)
            
            if not path_match or not operations_match:
                return self._format_error("Missing path or operations")
                
            path = path_match.group(1).strip()
            operations_json = operations_match.group(1).strip()
            
            # Parse operations JSON
            try:
                operations = json.loads(operations_json)
            except json.JSONDecodeError as e:
                return self._format_error(f"Invalid operations JSON: {str(e)}")
                
            if not isinstance(operations, list):
                return self._format_error("Operations must be a JSON array")
                
            # Validate operations
            for i, op in enumerate(operations):
                is_valid, error = validate_operation(op, i)
                if not is_valid:
                    return self._format_error(error)
                    
                # Validate regex pattern if enabled
                if op.get('use_regex', False):
                    is_valid, error = validate_regex_pattern(op['search'], i)
                    if not is_valid:
                        return self._format_error(error)
            
            # Read file
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
            except FileNotFoundError:
                return self._format_error(f"File not found: {path}")
            except Exception as e:
                return self._format_error(f"Error reading file: {str(e)}")
                
            # Apply operations
            modified = False
            for op in operations:
                start_line = op.get('start_line')
                end_line = op.get('end_line')
                use_regex = op.get('use_regex', False)
                ignore_case = op.get('ignore_case', False)
                
                # Determine line range
                start_idx = (start_line - 1) if start_line else 0
                end_idx = end_line if end_line else len(lines)
                
                # Prepare search pattern
                if use_regex:
                    flags = re.IGNORECASE if ignore_case else 0
                    pattern = re.compile(op['search'], flags)
                else:
                    search = op['search']
                    if ignore_case:
                        search = search.lower()
                
                # Apply replacement
                for i in range(start_idx, min(end_idx, len(lines))):
                    line = lines[i]
                    if use_regex:
                        new_line = pattern.sub(op['replace'], line)
                    else:
                        if ignore_case:
                            new_line = re.sub(re.escape(search), op['replace'], line, flags=re.IGNORECASE)
                        else:
                            new_line = line.replace(search, op['replace'])
                            
                    if new_line != line:
                        lines[i] = new_line
                        modified = True
            
            # Write changes if modified
            if modified:
                try:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.writelines(lines)
                except Exception as e:
                    return self._format_error(f"Error writing file: {str(e)}")
            
            return (
                "<replace>\n"
                f"  <path>{path}</path>\n"
                f"  <status>{'modified' if modified else 'unchanged'}</status>\n"
                "</replace>"
            )
            
        except Exception as e:
            logger.error(f"Replace operation error: {e}")
            return self._format_error(f"Error processing replace operation: {str(e)}")
            
    async def execute(self, input: str, **kwargs) -> str:
        """Execute the tool operation using simple tag parsing"""
        self.verbose = kwargs.get('verbose', False)
        
        if not input.startswith('<replace>'):
            return self._format_error("Invalid operation")
            
        return await self._handle_replace(input)

# Register the tool
registry.register(SearchReplaceTool()) 