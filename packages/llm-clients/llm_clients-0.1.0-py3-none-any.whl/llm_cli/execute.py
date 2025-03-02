"""
llm-execute: Execute tool operations with streaming support
"""
import asyncio
import logging
import re
import sys
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, AsyncGenerator, AsyncIterator, Any, Tuple, Union

import click
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.padding import Padding

from llm_cli.tools import registry

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(name)s] %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger("execute")

class BufferState(Enum):
    """State of a buffer segment"""
    STREAMING = "streaming"  # Still receiving input
    EXECUTING = "executing"  # Tool is currently executing
    DONE = "done"           # Ready to output

@dataclass
class BufferSegment:
    """A segment in the processing buffer"""
    content: str = ""
    tool_name: Optional[str] = None
    state: BufferState = BufferState.STREAMING
    result: Optional[Any] = None
    tag_stack: List[str] = field(default_factory=list)
    index: int = 0  # Position in the original stream

@dataclass
class ToolBlock:
    """Represents a tool block being built"""
    name: str
    params: Dict[str, str]
    content: List[str]
    complete: bool = False

class StreamingExecutor:
    """Handles streaming execution of tool blocks"""
    
    def __init__(self, verbose: bool = False, tool: Optional[Union[str, List[str]]] = None, 
                 history: Optional[str] = None, render_markdown: bool = True):
        self.verbose = verbose
        self.tools = [tool] if isinstance(tool, str) else tool  # Support multiple tools
        self.history = history  # History file path
        self.buffer: List[BufferSegment] = []
        self.next_index = 0  # For tracking segment order
        self.final_size = None  # To track when input is complete
        self.render_markdown = render_markdown
        self.processing_complete = False  # Flag to indicate all processing is done
        
        # Event loop and queues
        self.loop = asyncio.get_event_loop()
        self.input_queue: asyncio.Queue[Optional[str]] = asyncio.Queue()
        self.tool_queue: asyncio.Queue[Optional[Tuple[BufferSegment, Optional[int]]]] = asyncio.Queue()
        self.output_queue: asyncio.Queue[Optional[Tuple[Union[BufferSegment, Tuple[int, str]], Optional[int]]]] = asyncio.Queue()
        
        # Rich console for markdown rendering
        self.console = Console()
        
        # Get all registered XML tags from tools
        self.tag_patterns = {}
        self.tag_to_tool = {}
        
        if self.tools:
            # In direct tool mode, only get patterns from specified tools
            for tool_name in self.tools:
                tool = registry.get_tool(tool_name)
                if tool:
                    for tag_name in tool._xml_handlers.keys():
                        self.tag_patterns[tag_name] = re.compile(f'<{tag_name}>')
                        self.tag_to_tool[tag_name] = tool_name
        else:
            # Get patterns from all registered tools
            for tool_name, tool in registry._tools.items():
                for tag_name, pattern in tool._xml_patterns.items():
                    self.tag_patterns[tag_name] = pattern
                    self.tag_to_tool[tag_name] = tool_name
    
    def _get_or_create_segment(self) -> BufferSegment:
        """Get current streaming segment or create new one"""
        if not self.buffer or self.buffer[-1].state != BufferState.STREAMING:
            segment = BufferSegment(index=self.next_index)
            self.next_index += 1
            self.buffer.append(segment)
        return self.buffer[-1]
    
    def _find_start_tag(self, content: str) -> tuple[Optional[re.Match], Optional[str]]:
        """Find the earliest start tag in content"""
        start_match = None
        matched_tag = None
        
        # Look for start tags from the tag patterns we collected in __init__
        for tag_name, pattern in self.tag_patterns.items():
            match = pattern.search(content)
            if match and (not start_match or match.start() < start_match.start()):
                start_match = match
                matched_tag = tag_name
                
        return start_match, matched_tag
    
    def _find_end_tag(self, segment: BufferSegment) -> Optional[re.Match]:
        """Find end tag for the current tool"""
        if not segment.tag_stack:
            return None
        tag_name = segment.tag_stack[-1]
        pattern = re.compile(f'</{tag_name}>')
        return pattern.search(segment.content)
    
    async def start(self):
        """Start all processors"""
        self.processors = [
            self.loop.create_task(self.input_processor()),
            self.loop.create_task(self.tool_processor()),
            self.loop.create_task(self.output_processor())
        ]
    
    async def input_processor(self):
        """Process input chunks into buffer segments"""
        try:
            while True:
                chunk = await self.input_queue.get()
                try:
                    if chunk is None:  # EOF marker
                        # Process any remaining streaming segment
                        current = self._get_or_create_segment()
                        if current.state == BufferState.STREAMING and current.content:
                            current.state = BufferState.DONE
                            await self.tool_queue.put((current, None))
                        
                        # Now that all input is processed, set final size
                        self.final_size = len(self.buffer)
                        
                        # Signal end of tool processing
                        await self.tool_queue.put((None, self.final_size))
                        break
                    
                    # Process chunk into segments
                    current = self._get_or_create_segment()
                    current.content += chunk
                    
                    # Look for tags and split into segments
                    while True:
                        if current.state == BufferState.STREAMING:
                            start_match, matched_tag = self._find_start_tag(current.content)
                            if start_match:
                                # Split into text and tool segments
                                text_before = current.content[:start_match.start()]
                                tag_and_remaining = current.content[start_match.start():]
                                
                                if text_before:
                                    # Complete current segment with text before tag
                                    current.content = text_before
                                    current.state = BufferState.DONE
                                    await self.tool_queue.put((current, None))
                                    
                                    # Create new segment for tool content
                                    current = BufferSegment(index=self.next_index)
                                    self.next_index += 1
                                    self.buffer.append(current)
                                
                                # Set up tool segment
                                tool_name = self.tag_to_tool.get(matched_tag)
                                if tool_name and (not self.tools or tool_name in self.tools):
                                    current.tool_name = tool_name
                                    current.content = tag_and_remaining  # Keep the entire tag structure
                                    current.tag_stack.append(matched_tag)
                                    
                                    # Look for end tag immediately
                                    end_match = self._find_end_tag(current)
                                    if end_match:
                                        # Keep the complete XML structure including end tag
                                        tool_content = current.content[:end_match.end()]
                                        text_after = current.content[end_match.end():]
                                        
                                        # Update current segment for tool execution
                                        current.content = tool_content
                                        current.state = BufferState.EXECUTING
                                        await self.tool_queue.put((current, None))
                                        
                                        # Create new segment for remaining text
                                        if text_after:
                                            current = BufferSegment(
                                                content=text_after,
                                                index=self.next_index
                                            )
                                            self.next_index += 1
                                            self.buffer.append(current)
                                            continue
                                    break
                                else:
                                    # If tag doesn't match a valid tool, treat as regular text
                                    current.content = tag_and_remaining
                                    break
                            elif chunk == "":  # Final chunk
                                if current.content:  # Only if there's content
                                    current.state = BufferState.DONE
                                    await self.tool_queue.put((current, None))
                                break
                        break
                finally:
                    self.input_queue.task_done()
                    
        except Exception as e:
            logger.error(f"Input processor error: {e}")
            # Ensure tool processor gets EOF even on error
            await self.tool_queue.put((None, len(self.buffer)))
            raise
    
    async def tool_processor(self):
        """Execute tools on segments"""
        try:
            while True:
                item = await self.tool_queue.get()
                try:
                    if item is None or item[0] is None:  # EOF marker
                        # Signal end of output processing with final size
                        final_size = item[1] if item is not None else len(self.buffer)
                        await self.output_queue.put((None, final_size))
                        break
                    
                    segment, final_size = item
                    if segment.state == BufferState.EXECUTING:
                        if self.verbose:
                            logger.info(f"Executing {segment.tool_name}: {segment.content}")
                        
                        # Get tool and execute
                        tool = registry.get_tool(segment.tool_name)
                        if tool:
                            # Content already contains XML tags, no need to wrap again
                            segment.result = await tool.execute(
                                segment.content,
                                verbose=self.verbose
                            )
                            segment.state = BufferState.DONE
                            await self.output_queue.put((segment, final_size))
                        else:
                            logger.error(f"Tool not found: {segment.tool_name}")
                            segment.result = f"Error: Tool not found: {segment.tool_name}"
                            segment.state = BufferState.DONE
                            await self.output_queue.put((segment, final_size))
                    else:
                        # Non-executing segments go straight to output
                        await self.output_queue.put((segment, final_size))
                finally:
                    self.tool_queue.task_done()
                    
        except Exception as e:
            logger.error(f"Tool processor error: {e}")
            # Ensure output processor gets EOF even on error
            await self.output_queue.put((None, len(self.buffer)))
            raise
    
    async def output_processor(self):
        """Process output segments in order"""
        try:
            next_index = 0
            pending = {}
            output_buffer = []  # Buffer to collect all output
            
            while True:
                item = await self.output_queue.get()
                try:
                    if item is None or item[0] is None:  # EOF marker
                        # Save to history if specified
                        if self.history and output_buffer:
                            history_tool = registry.get_tool("history")
                            if history_tool:
                                full_output = "".join(output_buffer)
                                await history_tool.execute(
                                    full_output,
                                    history=self.history,
                                )
                                if self.verbose:
                                    logger.info(f"Saved to history: {self.history}")
                        self.processing_complete = True  # Signal completion
                        break
                    
                    segment, final_size = item
                    if isinstance(segment, BufferSegment):
                        content = segment.result or segment.content
                        pending[segment.index] = content
                        if self.verbose:
                            logger.info(f"Queued output for index {segment.index}: {content}")
                    else:
                        # Direct output tuple (index, content)
                        pending[segment[0]] = segment[1]
                        if self.verbose:
                            logger.info(f"Queued direct output for index {segment[0]}: {segment[1]}")
                    
                    # Output segments in order
                    while next_index in pending:
                        content = pending.pop(next_index)
                        output_buffer.append(content)  # Add to buffer for history
                        if not self.render_markdown:
                            print(content, end="", flush=True)
                        next_index += 1
                finally:
                    self.output_queue.task_done()
                    
        except Exception as e:
            logger.error(f"Output processor error: {e}")
            raise
    
    async def markdown_renderer(self):
        """Render markdown output in real-time"""
        if not self.render_markdown:
            return
            
        try:
            with Live(auto_refresh=False, console=self.console) as live:
                while not self.processing_complete:
                    # Simply show current content of all segments in order
                    output = []
                    for seg in sorted(self.buffer, key=lambda x: x.index):
                        output.append(seg.result or seg.content)
                    
                    # Render markdown
                    content = "".join(output)
                    try:
                        markdown = Markdown(content)
                        live.update(Padding(markdown, (1, 2)))
                    except:
                        live.update(content)
                    live.refresh()
                    
                    await asyncio.sleep(0.8)
                    
                # One final update after completion
                output = []
                for seg in sorted(self.buffer, key=lambda x: x.index):
                    output.append(seg.result or seg.content)
                content = "".join(output)
                try:
                    markdown = Markdown(content)
                    live.update(Padding(markdown, (1, 2)))
                except:
                    live.update(content)
                live.refresh()
                    
        except Exception as e:
            logger.error(f"Markdown renderer error: {e}")
            raise

    async def process_stream(self, input_stream: AsyncIterator[str]) -> None:
        """Process the input stream"""
        try:
            # Start processors
            if self.verbose:
                logger.info("Started processors")
            
            # Create tasks for processors
            input_task = asyncio.create_task(self.input_processor())
            tool_task = asyncio.create_task(self.tool_processor())
            output_task = asyncio.create_task(self.output_processor())
            markdown_task = asyncio.create_task(self.markdown_renderer())
            
            # Feed input chunks
            try:
                async for chunk in input_stream:
                    await self.input_queue.put(chunk)
            except Exception as e:
                logger.error(f"Error reading input stream: {e}")
                raise
            finally:
                # Signal end of input
                await self.input_queue.put(None)
                if self.verbose:
                    logger.info("Input stream complete")
            
            # Wait for all queues to be empty
            await self.input_queue.join()
            await self.tool_queue.join()
            await self.output_queue.join()
            
            # Wait for all processors to complete and handle any exceptions
            try:
                await asyncio.gather(input_task, tool_task, output_task, markdown_task)
            except Exception as e:
                logger.error(f"Processor error during cleanup: {e}")
                # Cancel any remaining tasks
                for task in [input_task, tool_task, output_task, markdown_task]:
                    if not task.done():
                        task.cancel()
                raise
                
            if self.verbose:
                logger.info("All queues processed")
                
        except Exception as e:
            logger.error(f"Process stream error: {e}")
            raise

async def execute_tool(
    input: str,
    tool_name: str,
    verbose: bool = False,
    history: Optional[str] = None,
    render_markdown: bool = True,
) -> str:
    """Execute a tool operation
    
    Args:
        input: Input text
        tool_name: Name of the tool to use
        verbose: Whether to log details
        history: Optional history file path
        render_markdown: Whether to render markdown
        
    Returns:
        Operation result string
        
    Raises:
        ValueError: If tool is not available
        Exception: For other errors during processing
    """
    # Get the tool
    tool = registry.get_tool(tool_name)
    if not tool:
        raise ValueError(f"Tool not found: {tool_name}")
        
    logger.info(f"Executing tool: {tool_name}")
    logger.info(f"Input: {input}")
        
    try:
        # Execute the tool
        result = await tool.execute(input, verbose=verbose)
        logger.info(f"Tool returned: {result}")
        
        # Save to history if specified and not using history tool
        if history and tool_name != "history":
            history_tool = registry.get_tool("history")
            if history_tool:
                await history_tool.execute(
                    result,
                    history=history,
                    role="assistant",
                )
                if verbose:
                    logger.info(f"Saved to history: {history}")
        
        if verbose:
            logger.info(f"Tool execution complete: {len(result)} chars")
        return result
        
    except Exception as e:
        logger.error(f"Error executing tool: {e}")
        raise

async def stream_stdin() -> AsyncGenerator[str, None]:
    """Stream input from stdin"""
    loop = asyncio.get_event_loop()
    while True:
        line = await loop.run_in_executor(None, sys.stdin.readline)
        if not line:
            break
        yield line

@click.command()
@click.argument('text', required=False)
@click.option('--tool', '-t', multiple=True, help='Tool(s) to execute')
@click.option('--history', '-H', help='History file')
@click.option('--verbose', '-v', is_flag=True, help='Show verbose output')
@click.option('--debug', is_flag=True, help='Enable debug logging')
@click.option('--no-markdown', is_flag=True, help='Disable markdown rendering')
def main(
    text: Optional[str],
    tool: Optional[List[str]],
    history: Optional[str],
    verbose: bool,
    debug: bool,
    no_markdown: bool,
):
    """Execute tool operations with streaming support.
    
    Input is read from stdin if no text argument is provided.
    Output is always written to stdout.
    
    Examples:\n
        # Execute single tool \n
        $ echo "<replace>...</replace>" | llm-execute -t replace \n
        
        # Execute multiple tools \n
        $ echo "<calculator>2+2</calculator>" | llm-execute -t calculator -t file \n
        
        # Show progress \n
        $ echo "<replace>...</replace>" | llm-execute -v -t replace\n
        
        # With history \n
        $ llm-prompt -h chat.log | llm-query -h chat.log | llm-execute -h chat.log\n
    """
    if debug:
        logger.setLevel(logging.DEBUG)
    elif verbose:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.WARNING)
        
    try:
        async def main_async():
            # Convert empty tuple to None for consistency
            tools = list(tool) if tool else None
            executor = StreamingExecutor(verbose=verbose, tool=tools, history=history, render_markdown=not no_markdown)
            await executor.process_stream(stream_stdin())
                
        asyncio.run(main_async())
            
    except Exception as e:
        logger.error(f"Error executing tool: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()