"""
Main CLI interface for llm-clients
"""
import os
import sys
from pathlib import Path
from typing import List, Optional
import warnings
import shlex
import yaml

import click
from rich.console import Console
from rich.table import Table

from llm_cli import __version__
from llm_cli.config import config as config_instance, DEFAULT_CONFIG
# Import all tools to register them
from llm_cli.tools import registry

# Suppress Pydantic warning about built-in function types
warnings.filterwarnings("ignore", message=".*is not a Python type.*")
console = Console()

@click.group()
@click.version_option(version=__version__)
def main():
    """LLM Clients - Command line utilities for working with Large Language Models"""
    pass

@main.group()
def config():
    """Configuration management"""
    pass

@config.command()
@click.argument("key")
@click.argument("value")
def set(key: str, value: str):
    """Set a configuration value"""
    try:
        config_instance.set(key, value)
        console.print(f"[green]Set {key} = {value}[/green]")
    except Exception as e:
        console.print(f"[red]Error setting config: {e}[/red]")
        sys.exit(1)

@config.command()
@click.argument("key")
def get(key: str):
    """Get a configuration value"""
    try:
        value = config_instance.get(key)
        if value is None:
            console.print(f"[yellow]No value set for {key}[/yellow]")
        else:
            console.print(str(value))
    except Exception as e:
        console.print(f"[red]Error getting config: {e}[/red]")
        sys.exit(1)

@config.command()
def init():
    """Initialize default configuration file"""
    try:
        config_path = Path.home() / ".config" / "llm-clients"
        config_file = config_path / "config.yaml"
        
        # Create config directory if it doesn't exist
        config_path.mkdir(parents=True, exist_ok=True)
        
        # Don't overwrite existing config
        if config_file.exists():
            console.print("[yellow]Config file already exists at ~/.config/llm-clients/config.yaml[/yellow]")
            return
        
        # Write default config
        with open(config_file, "w") as f:
            yaml.dump(DEFAULT_CONFIG, f, default_flow_style=False)
        
        console.print(f"[green]Created default config at {config_file}[/green]")
    except Exception as e:
        console.print(f"[red]Error initializing config: {e}[/red]")
        sys.exit(1)

@main.group()
def tools():
    """Tool lifecycle management"""
    pass

@tools.command()
def list():
    """List available tools"""
    try:
        # Create a table for display
        table = Table(title="Available Tools")
        table.add_column("Name", style="cyan")
        table.add_column("Description", style="green")
        
        # Add each tool to the table
        tools = registry.list_tools()
        for tool in sorted(tools, key=lambda x: x["name"]):
            table.add_row(tool["name"], tool["description"])
            
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]Error listing tools: {e}[/red]")
        sys.exit(1)

@main.command(
    epilog="For more examples and documentation, visit: https://github.com/PsychArch/llm-clients",
    context_settings=dict(help_option_names=['-h', '--help'])
)
@click.argument("text", required=False, metavar="<text>")
@click.option("-f", "--file", type=click.File("r"), metavar="<file>", help="Read input from file")
@click.option("-t", "--tool", multiple=True, metavar="<n>", help="Tool to use (can specify multiple)")
@click.option("-m", "--model", metavar="<n>", help="Model to use")
@click.option("-o", "--output", type=click.File("w"), metavar="<file>", help="Write output to file")
@click.option("--web", is_flag=True, help="Enable web search/grounding")
@click.option("--image", multiple=True, type=click.Path(exists=True), help="Path to image file")
@click.option("--image-detail", type=click.Choice(['low', 'high', 'auto']), default='high', help="Image detail level")
@click.option("--no-render", is_flag=True, help="Disable markdown rendering")
@click.option("-v", "--verbose", is_flag=True, help="Show verbose output")
@click.option("-H", "--history", metavar="<history>", help="History file")
def run(
    text: Optional[str],
    file: Optional[click.File],
    tool: Optional[tuple],
    model: Optional[str],
    output: Optional[click.File],
    web: bool,
    image: tuple,
    image_detail: str,
    no_render: bool,
    verbose: bool,
    history: Optional[str],
):
    """Run the LLM pipeline with optional tools and model selection.
    
    If no text argument is provided, input is read from stdin.
    Output is written to stdout unless -o/--output is specified.
    
    Examples:
      Basic Usage:
        Simple calculation:
          $ llm run "Calculate 2+2" -t calculator
    
        File input:
          $ llm run -f input.txt -t calculator
    
      Advanced Usage:
        Multiple tools:
          $ llm run "Find bugs" -t search_replace -t fix
    
        Custom model:
          $ llm run "Translate to French" -m gpt4
        
        Web search:
          $ llm run "Latest news about AI" --web
        
        Image input:
          $ llm run "What's in this image?" --image photo.jpg
        
        Multiple images:
          $ llm run "Compare these images" --image img1.jpg --image img2.jpg
    
        Save output:
          $ llm run "Generate code" -o output.py
    
        Verbose mode:
          $ llm run -v "Calculate 2+2" -t calculator
    """
    try:
        # Get input text and instruction
        if file:
            instruction = text if text else "Process this file"
            input_source = f"-f {file.name}"
        elif text:
            instruction = text
            input_source = ""
        else:
            instruction = "Process this input"
            input_source = ""  # Will read from stdin
            
        # Build pipeline commands
        prompt_cmd = ["llm-prompt"]
        if tool:
            for t in tool:
                prompt_cmd.extend(["-t", t])
        if history:
            prompt_cmd.extend(["-H", history])
        if input_source:
            prompt_cmd.append(input_source)
        # Always quote the instruction to handle special characters
        prompt_cmd.extend(["--instruct", shlex.quote(instruction)])
        
        query_cmd = ["llm-query"]
        if model:
            query_cmd.extend(["-m", model])
        if web:
            query_cmd.append("--web")
        for img in image:
            query_cmd.extend(["--image", str(img)])
        if image:
            query_cmd.extend(["--image-detail", image_detail])
            
        execute_cmd = ["llm-execute"]
        if tool:
            for t in tool:
                execute_cmd.extend(["-t", t])
        if history:
            execute_cmd.extend(["-H", history])
        if no_render:
            execute_cmd.append("--no-markdown")
            
        # Add verbose flag if needed
        if verbose:
            prompt_cmd.append("-v")
            query_cmd.append("-v")
            execute_cmd.append("-v")
            
        # Combine commands into a pipeline
        pipeline_cmd = " | ".join([
            " ".join(f'"{arg}"' if " " in arg else arg for arg in cmd)
            for cmd in [prompt_cmd, query_cmd, execute_cmd]
        ])
        
        if verbose:
            console.print(f"\n[blue]Running pipeline:[/blue] {pipeline_cmd}")
            
        # Execute the pipeline using os.system
        return_code = os.system(pipeline_cmd)
        
        if return_code != 0:
            sys.exit(return_code >> 8)  # Get the actual exit code from the shell
            
    except Exception as e:
        console.print(f"[red]Error running pipeline: {e}[/red]")
        sys.exit(1)

@main.command()
def list_models():
    """List available models and their aliases"""
    try:
        # Create a table for display
        table = Table(title="Available Models")
        table.add_column("Alias", style="cyan")
        table.add_column("Provider", style="green")
        table.add_column("Model", style="yellow")
        
        # Get aliases from config
        aliases = config_instance.get("models.aliases") or {}
        
        # Add each model to the table
        for alias, target in sorted(aliases.items()):
            try:
                provider, model_name, _ = config_instance.resolve_model(alias)
                table.add_row(alias, provider, model_name)
            except ValueError as e:
                table.add_row(alias, "error", str(e))
            
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]Error listing models: {e}[/red]")
        sys.exit(1)

if __name__ == "__main__":
    main()