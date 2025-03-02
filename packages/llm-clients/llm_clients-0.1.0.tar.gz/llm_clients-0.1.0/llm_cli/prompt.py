"""
llm-prompt: Generate prompts using tools
"""
import asyncio
import logging
import sys
import warnings
from pathlib import Path
from typing import List, Optional, Tuple

import click

from llm_cli.tools import Tool, registry
# Tools are automatically imported by the tools package

# Suppress Pydantic warning about built-in function types
warnings.filterwarnings("ignore", message=".*is not a Python type.*")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(name)s] %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger("prompt")

async def generate_prompt(
    context: str = "",
    instruct: Optional[str] = None,
    history: Optional[str] = None,
    tools: Optional[List[str]] = None,
    files: Optional[List[str]] = None,
    verbose: bool = False,
    **kwargs
) -> str:
    """Generate a prompt using the specified tools
    
    Args:
        context: Context from stdin
        instruct: Request from --instruct
        history: Optional path to history file
        tools: Optional list of tools to use
        files: Optional list of files to read
        verbose: Whether to log details
        **kwargs: Additional tool-specific parameters
        
    Returns:
        Generated prompt string
    """
    sections = []
    
    # Log inputs if verbose
    if verbose:
        if tools:
            logger.info(f"Using tools: {', '.join(tools)}")
        if files:
            logger.info(f"Reading files: {', '.join(files)}")
        if context:
            logger.info(f"Context length: {len(context)} chars")
        if instruct:
            logger.info(f"Request: {instruct}")
        if history:
            logger.info(f"History file: {history}")
    
    # Add tool-specific instructions for each tool specified
    if tools:
        for tool_name in tools:
            tool_instance = registry.get_tool(tool_name)
            if tool_instance:
                # Use instruct for tool prompt if available
                tool_prompt = await tool_instance.generate_prompt(instruct or "", **kwargs)
                sections.append(f"==== {tool_name.title()} Tool Usage ====\n" + tool_prompt)
                if verbose:
                    logger.info(f"Added {tool_name} tool usage section: {len(tool_prompt)} chars")
    
    # Add file contents if provided
    if files:
        sections.append("==== File Contents ====")
        file_tool = registry.get_tool("file")
        if file_tool:
            for file_path in files:
                sections.append(f"Contents of {file_path}:")
                # Create XML read_file tag and execute it
                xml_content = f"<read_file><path>{file_path}</path></read_file>"
                file_content = await file_tool.execute(xml_content)
                sections.append(file_content)
                if verbose:
                    logger.info(f"Added file contents for: {file_path}")
    
    # Add history context if provided
    if history:
        history_tool = registry.get_tool("history")
        if history_tool:
            history_prompt = await history_tool.generate_prompt(
                instruct or "",
                history=history,
                **kwargs
            )
            sections.append("==== Conversation History ====\n" + history_prompt)
            if verbose:
                logger.info(f"Added history section: {len(history_prompt)} chars")
    
    # Add context from stdin if available
    if context:
        sections.append("==== Context ====\n" + context)
        if verbose:
            logger.info(f"Added context section: {len(context)} chars")
    
    # Add request from --instruct if available
    if instruct:
        sections.append("==== Current Request ====\n" + instruct)
        if verbose:
            logger.info("Added request section")
    
    result = "\n\n".join(sections)
    if verbose:
        logger.info(f"Generated prompt: {len(result)} chars total")
    return result

@click.command(
    epilog="For more examples and documentation, visit: https://github.com/PsychArch/llm-cli",
    context_settings=dict(help_option_names=['-h', '--help'])
)
@click.option(
    "-H", "--history",
    type=click.Path(dir_okay=False, writable=True, resolve_path=True),
    metavar="<file>",
    help="Path to history file (will be created if it doesn't exist)"
)
@click.option("--instruct", metavar="<text>", help="Request to process")
@click.option("-t", "--tool", multiple=True, metavar="<n>", help="Tool to use (e.g. calculator, file). Can be specified multiple times")
@click.option("-f", "--read-file", multiple=True, metavar="<file>", help="File to read and include in prompt. Can be specified multiple times")
@click.option("-v", "--verbose", is_flag=True, help="Show verbose output")
@click.option("--debug", is_flag=True, help="Enable debug logging")
def main(
    history: Optional[str],
    instruct: Optional[str],
    tool: Optional[tuple],
    read_file: Optional[tuple],
    verbose: bool,
    debug: bool,
):
    """Generate prompts with optional tool instructions and history.
    
    The command accepts input in two ways:
    1. From stdin (piped input)
    2. Via the --instruct option
    
    If both are provided, stdin is treated as context and --instruct as the current request.
    If only stdin is provided, it is treated as the request.
    
    Examples:\n
        # Use stdin as request \n
        $ echo "Calculate 2+2" | llm-prompt \n
        
        # Use stdin as context with instruction \n
        $ cat file.txt | llm-prompt --instruct "Summarize this text" \n
        
        # Use instruction only \n
        $ llm-prompt --instruct "Calculate 2+2" \n
        
        # Add tool instructions \n
        $ llm-prompt -t calculator --instruct "Calculate 2+2" \n
        
        # Use multiple tools \n
        $ llm-prompt -t calculator -t file --instruct "Calculate 2+2 and save to result.txt" \n
        
        # Include file contents \n
        $ llm-prompt -f code.py --instruct "Fix the bugs in this code" \n
        
        # Combine file contents with tools \n
        $ llm-prompt -f code.py -t file --instruct "Fix the bugs and save the changes" \n
        
        # With history \n
        $ llm-prompt -H chat.log --instruct "What was my last question?" \n
    """
    if debug:
        logger.setLevel(logging.DEBUG)
    elif verbose:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.WARNING)
        
    try:
        # Get context from stdin if available
        context = ""
        if not sys.stdin.isatty():
            if verbose:
                logger.info("Reading from stdin")
            context = sys.stdin.read().strip()
            
        # If no instruct is provided but we have stdin content, use it as the instruction
        if not instruct and context:
            instruct = context
            context = ""
            if verbose:
                logger.info("Using stdin content as instruction")
            
        # Convert tool tuple to list if specified
        tools = list(tool) if tool else None
        
        # Convert read_file tuple to list if specified
        files = list(read_file) if read_file else None
            
        # Generate prompt with tools if specified
        text = asyncio.run(generate_prompt(
            context=context,
            instruct=instruct,
            history=history,
            tools=tools,
            files=files,
            verbose=verbose
        ))
            
        # Write prompt to stdout
        print(text)
        
    except Exception as e:
        logger.error(f"Error generating prompt: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()