"""
History management tool for LLM interactions
"""
import logging
from pathlib import Path
from typing import List, Optional

from llm_cli.tools import Tool, registry

logger = logging.getLogger(__name__)

class History:
    """Manages conversation history in plain text format"""
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.entries: List[tuple[str, str]] = []  # [(role, content), ...]
        
        # Create parent directory if it doesn't exist
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create empty file if it doesn't exist
        if not self.file_path.exists():
            self.file_path.touch()
            logger.info(f"Created new history file: {self.file_path}")
            
        self._load()

    def _load(self):
        """Load history from file"""
        self.entries = []
        if not self.file_path.exists():
            return

        try:
            current_role = None
            current_content = []
            
            with open(self.file_path, 'r') as f:
                for line in f:
                    line = line.rstrip('\n')
                    if line == '<history>' or line == '</history>':
                        continue
                    if line.startswith(('User: ', 'Assistant: ')):
                        # Save previous entry if exists
                        if current_role and current_content:
                            self.entries.append((current_role, '\n'.join(current_content)))
                            current_content = []
                        # Start new entry
                        role, content = line.split(': ', 1)
                        current_role = 'user' if role == 'User' else 'assistant'
                        current_content = [content] if content else []
                    elif current_content is not None:
                        current_content.append(line)
                        
            # Save last entry
            if current_role and current_content:
                self.entries.append((current_role, '\n'.join(current_content)))
                
        except Exception as e:
            logger.error(f"Error loading history: {e}")
            self.entries = []

    def save(self):
        """Save history to file"""
        try:
            with open(self.file_path, 'w') as f:
                f.write('<history>\n')
                for role, content in self.entries:
                    display_role = 'Assistant' if role == 'assistant' else 'User'
                    f.write(f'{display_role}: {content}\n')
                f.write('</history>\n')
        except Exception as e:
            logger.error(f"Error saving history: {e}")

    def add_message(self, role: str, content: str):
        """Add a message to history
        
        Args:
            role: Either 'user' or 'assistant'
            content: Message content
        """
        content = content.strip()
        if not content:
            return
            
        # Don't add duplicate messages
        if self.entries and self.entries[-1] == (role, content):
            return
            
        self.entries.append((role, content))
        self.save()

    def append_assistant_response(self, response: str):
        """Append an assistant's response to history"""
        self.add_message('assistant', response)

    def get_context_with_prompt(self, user_message: Optional[str] = None) -> str:
        """Get history with optional user message and prompt context"""
        if not self.entries and not user_message:
            return "This is a new conversation.\n\n<history>\n</history>"
            
        # Add new user message first if provided
        if user_message:
            self.add_message('user', user_message)
            
        lines = ['This is a conversation history. Please continue the conversation.\n']
        lines.append('<history>')
        
        # Add existing history
        for role, content in self.entries:
            display_role = 'Assistant' if role == 'assistant' else 'User'
            lines.append(f'{display_role}: {content}')
            
        lines.append('</history>')
        return '\n'.join(lines)

class HistoryTool(Tool):
    """Tool for managing conversation history"""
    
    @property
    def name(self) -> str:
        return "history"

    @property
    def description(self) -> str:
        return "Manages conversation history and contextual information"

    async def generate_prompt(self, input: str, **kwargs) -> str:
        """Generate a prompt with history context"""
        history_file = kwargs.get("history")
        if not history_file:
            # If no history file, just format the input message
            return f"User: {input}"
            
        # Get history with context
        history = History(Path(history_file))
        return history.get_context_with_prompt(input)

    async def execute(self, input: str, **kwargs) -> str:
        """Execute history operations (primarily for appending assistant responses)"""
        history_file = kwargs.get("history")
        if not history_file:
            # History file is optional for execute
            return input
            
        history = History(Path(history_file))
        history.append_assistant_response(input)
        return input

# Register the tool
registry.register(HistoryTool())