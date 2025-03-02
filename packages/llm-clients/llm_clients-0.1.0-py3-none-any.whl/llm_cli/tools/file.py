"""
File system operations tool with XML-based interface

Supports operations:
1. Write file: <write_file><path>file.txt</path><content>data</content></write_file>
2. Read file: <read_file><path>file.txt</path></read_file>

The tool provides robust error handling and validation for all operations.
"""
import os
from pathlib import Path
import logging
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape, unescape
import re

from llm_cli.tools import Tool, registry
from llm_cli.tools.decorators import register_tool

logger = logging.getLogger(__name__)

@register_tool
class FileTool(Tool):
    """Tool for file system operations using XML format"""
    
    def __init__(self):
        """Initialize tool and register XML tag handlers"""
        super().__init__()
        self.register_xml_tag('write_file', self._handle_write_file)
        self.register_xml_tag('read_file', self._handle_read_file)
    
    @property
    def name(self) -> str:
        return "file"
        
    @property
    def description(self) -> str:
        return "File operations (read/write) using XML tags"
        
    async def generate_prompt(self, input: str, **kwargs) -> str:
        """Generate a prompt instructing LLM to use file operation tags"""
        cwd = str(Path.cwd())
        return (
            "## File System Operations Tool\n\n"
            "Description: This tool provides read and write operations for files. All operations MUST be wrapped in XML tags.\n\n"
            "Available Operations:\n\n"
            "1. Write File Operation\n"
            "Description: Write content to a file. If the file exists, it will be overwritten. If it doesn't exist, it will be created.\n"
            "Parameters:\n"
            f"- path: (required) The path of the file to write to (relative to {cwd})\n"
            "- content: (required) The COMPLETE content to write to the file. Provide the raw content exactly as it should appear in the file.\n"
            "  DO NOT escape any special characters - the tool will handle that internally.\n"
            "Format:\n"
            "<write_file>\n"
            "<path>file_path_here</path>\n"
            "<content>\n"
            "Your raw content here, exactly as it should appear in the file\n"
            "</content>\n"
            "</write_file>\n\n"
            "Example - Writing a C++ header file:\n"
            "<write_file>\n"
            "<path>example.h</path>\n"
            "<content>\n"
            "#ifndef EXAMPLE_H\n"
            "#define EXAMPLE_H\n"
            "\n"
            "#include <vector>\n"
            "#include <string>\n"
            "\n"
            "class Example {\n"
            "public:\n"
            "    Example() = default;\n"
            "    void process(const std::vector<std::string>& input);\n"
            "};\n"
            "\n"
            "#endif // EXAMPLE_H\n"
            "</content>\n"
            "</write_file>\n\n"
            "2. Read File Operation\n"
            "Description: Read the contents of a file.\n"
            "Parameters:\n"
            f"- path: (required) The path of the file to read (relative to {cwd})\n"
            "Format:\n"
            "<read_file>\n"
            "<path>file_path_here</path>\n"
            "</read_file>\n\n"
            "Important Rules:\n"
            "1. DO NOT escape special characters in file content - provide it exactly as it should appear\n"
            "2. NEVER truncate or omit parts of the file content\n"
            "3. Use relative paths when possible\n"
            "4. The tool will automatically create directories if needed\n"
            "5. Make sure to include proper line endings (\\n) in the content\n\n"
            f"Now please help with this request: {input}"
        )

    def _format_error(self, operation: str, message: str) -> str:
        """Format error response in XML"""
        return (
            f"<{operation}>\n"
            "  <error>\n"
            f"    {escape(message)}\n"
            "  </error>\n"
            f"</{operation}>"
        )

    def _validate_path(self, path: str) -> tuple[bool, str]:
        """Validate file path and convert to absolute path if needed
        
        Returns:
            Tuple of (is_valid, error_message or absolute_path)
        """
        if not path:
            return False, "Empty file path"
            
        try:
            # Convert to Path object and resolve to absolute path if needed
            file_path = Path(path)
            if not file_path.is_absolute():
                # For relative paths, resolve against current working directory
                file_path = Path.cwd() / file_path
            
            # Resolve to absolute path, removing any .. or . components
            abs_path = file_path.resolve()
            
            # Verify the resolved path is under the current directory
            try:
                abs_path.relative_to(Path.cwd())
                return True, str(abs_path)
            except ValueError:
                return False, "Path must be within current working directory"
                
        except Exception as e:
            return False, f"Invalid path: {str(e)}"
    
    async def _handle_write_file(self, content: str) -> str:
        """Handle write_file operation using simple tag parsing"""
        try:
            # Find path and content using simple patterns
            path_match = re.search(r'<path>(.*?)</path>', content, re.DOTALL)
            content_match = re.search(r'<content>(.*?)</content>', content, re.DOTALL)
            
            if not path_match or not content_match:
                return self._format_error("write_file", "Missing path or content element")
                
            path = path_match.group(1).strip()
            file_content = content_match.group(1)
            
            logger.info(f"Processing write request for path: {path}")
            
            # Validate path
            is_valid, result = self._validate_path(path)
            if not is_valid:
                logger.error(f"Path validation failed: {result}")
                return self._format_error("write_file", result)
            
            # Use the validated absolute path
            file_path = Path(result)
            logger.info(f"Resolved path: {file_path}")
            
            # Create parent directories if needed
            try:
                logger.info(f"Creating parent directories: {file_path.parent}")
                file_path.parent.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                logger.error(f"Failed to create directories for {path}: {e}")
                return self._format_error("write_file", f"Failed to create directories: {str(e)}")
            
            # Write file
            try:
                logger.info(f"Writing content to file: {file_path}")
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(file_content)
                logger.info("File write successful")
                    
                return (
                    "<write_file>\n"
                    f"  <path>{path}</path>\n"
                    "  <status>success</status>\n"
                    "</write_file>"
                )
            except PermissionError:
                logger.error(f"Permission denied writing to {file_path}")
                return self._format_error("write_file", f"Do not have permission to write to {path}")
            except OSError as e:
                logger.error(f"OS error writing to {file_path}: {e}")
                return self._format_error("write_file", f"Error writing to file: {str(e)}")
                
        except Exception as e:
            logger.error(f"Write operation error: {e}")
            return self._format_error("write_file", f"Error processing write operation: {str(e)}")

    async def execute(self, input: str, **kwargs) -> str:
        """Execute the tool operation
        
        Instead of using XML parsing, use simple tag-based parsing
        """
        self.verbose = kwargs.get('verbose', False)
        
        # Find the operation (write_file or read_file)
        if input.startswith('<write_file>'):
            handler = self._handle_write_file
        elif input.startswith('<read_file>'):
            handler = self._handle_read_file
        else:
            return "Error: Invalid operation"
            
        # Call the appropriate handler with the raw content
        return await handler(input)

    async def _handle_read_file(self, content: str) -> str:
        """Handle read_file operation using simple tag parsing"""
        try:
            # Find path using simple pattern
            path_match = re.search(r'<path>(.*?)</path>', content, re.DOTALL)
            if not path_match:
                return self._format_error("read_file", "Missing path element")
                
            path = path_match.group(1).strip()
            
            # Validate path
            is_valid, result = self._validate_path(path)
            if not is_valid:
                return self._format_error("read_file", result)
                
            # Use the validated absolute path
            file_path = Path(result)
            if not file_path.exists():
                return self._format_error("read_file", f"File not found: {path}")
            if not file_path.is_file():
                return self._format_error("read_file", f"Path is not a file: {path}")
                
            # Read file
            try:
                if self.verbose:
                    logger.info(f"Reading file: {file_path}")
                    
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Format response
                return (
                    "<read_file>\n"
                    f"  <path>{path}</path>\n"
                    "  <content>\n"
                    f"{content}\n"
                    "  </content>\n"
                    "</read_file>"
                )
            except PermissionError:
                return self._format_error("read_file", f"Do not have permission to read {path}")
            except OSError as e:
                return self._format_error("read_file", f"Error reading file: {str(e)}")
                
        except Exception as e:
            logger.error(f"Read operation error: {e}")
            return self._format_error("read_file", f"Error processing read operation: {str(e)}")

# Register the tool
registry.register(FileTool()) 