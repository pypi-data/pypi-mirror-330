"""
Markdown rendering utilities for llm-cli
"""
from typing import Optional, TextIO
import sys
import click
from rich.console import Console
from rich.markdown import Markdown
import io
from rich.padding import Padding
from rich.live import Live
import time

def render_markdown_stream(
    input_stream: Optional[TextIO] = None,
    render_interval: float = 0.8,
    padding: tuple = (1, 2)
) -> None:
    """
    Renders markdown input from a stream with live updates.
    
    Args:
        input_stream: Input stream to read from (defaults to sys.stdin)
        render_interval: Minimum time between renders in seconds
        padding: Tuple of (vertical, horizontal) padding values
    """
    console = Console()
    buffer = io.StringIO()
    last_render = 0
    input_stream = input_stream or sys.stdin
    
    try:
        with Live(auto_refresh=False, console=console) as live:
            # Read and render line by line
            for line in input_stream:
                buffer.write(line)
                current_time = time.time()
                
                # Only render if enough time has passed
                if current_time - last_render >= render_interval:
                    try:
                        markdown = Markdown(buffer.getvalue())
                        live.update(Padding(markdown, padding))
                        live.refresh()
                        last_render = current_time
                    except:
                        continue
            
            # Final render
            try:
                markdown = Markdown(buffer.getvalue())
                live.update(Padding(markdown, padding))
                live.refresh()
            except:
                pass
                
    except Exception as e:
        click.echo(f"Error rendering markdown: {str(e)}", err=True)
        sys.exit(1)

def render_markdown_text(
    text: str,
    padding: tuple = (1, 2)
) -> None:
    """
    Renders markdown text directly.
    
    Args:
        text: Markdown text to render
        padding: Tuple of (vertical, horizontal) padding values
    """
    console = Console()
    try:
        markdown = Markdown(text)
        console.print(Padding(markdown, padding))
    except Exception as e:
        click.echo(f"Error rendering markdown: {str(e)}", err=True)
        sys.exit(1)

@click.command()
@click.help_option('--help', '-h')
@click.option('--interval', '-i', type=float, default=0.8,
              help='Render interval in seconds (default: 0.8)')
@click.option('--padding-v', type=int, default=1,
              help='Vertical padding (default: 1)')
@click.option('--padding-h', type=int, default=2,
              help='Horizontal padding (default: 2)')
def main(interval: float, padding_v: int, padding_h: int):
    """
    Renders markdown input from stdin with live updates.
    
    Usage:
        echo "# Hello" | llm-md-render
        cat README.md | llm-md-render
        tail -f README.md | llm-md-render
        
    Press Ctrl+C to exit
    """
    try:
        render_markdown_stream(
            render_interval=interval,
            padding=(padding_v, padding_h)
        )
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)

if __name__ == '__main__':
    main() 