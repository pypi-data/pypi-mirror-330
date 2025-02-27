"""
EPUB-related commands for Hermano CLI.
"""

import json
import os
from pathlib import Path

import click
import ebooklib
import tiktoken
from bs4 import BeautifulSoup
from ebooklib import epub as epub_lib
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


@click.group(name="epub")
def epub():
    """Commands for working with EPUB files."""
    pass


@epub.command(name="tokens")
@click.argument("epub_path", type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.option(
    "--model",
    type=str,
    default="gpt-4",
    help="Model to calculate tokens for (default: gpt-4)",
)
@click.option(
    "--format",
    type=click.Choice(["text", "json"]),
    default="text",
    help="Output format (text, json)",
)
@click.pass_context
def count_tokens(ctx, epub_path, model, format):
    """Calculate the number of tokens in an EPUB file for a given LLM model."""
    try:
        # Get appropriate tokenizer
        try:
            tokenizer = tiktoken.encoding_for_model(model)
        except KeyError:
            # Fall back to cl100k_base for models not in tiktoken
            tokenizer = tiktoken.get_encoding("cl100k_base")
            console.print(f"[yellow]Warning:[/yellow] Model {model} not found in tiktoken, using cl100k_base")

        # Process EPUB file
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Reading EPUB file...", total=None)
            
            # Load EPUB
            book = epub_lib.read_epub(epub_path)
            
            # Extract text from EPUB items
            total_text = ""
            progress.update(task, description="Extracting text...")
            
            for item in book.get_items():
                if item.get_type() == ebooklib.ITEM_DOCUMENT:
                    # Parse HTML content
                    soup = BeautifulSoup(item.get_content(), "html.parser")
                    
                    # Extract and clean text
                    content_text = soup.get_text(separator=" ", strip=True)
                    total_text += content_text + "\n\n"
            
            # Count tokens
            progress.update(task, description="Counting tokens...")
            tokens = tokenizer.encode(total_text)
            token_count = len(tokens)
            
            # Get file size information
            file_size = Path(epub_path).stat().st_size
            file_size_mb = file_size / (1024 * 1024)
            
            # Calculate average tokens per MB
            tokens_per_mb = int(token_count / file_size_mb) if file_size_mb > 0 else 0
        
        # Output results
        if format == "json":
            result = {
                "file_path": epub_path,
                "model": model,
                "token_count": token_count,
                "file_size_bytes": file_size,
                "file_size_mb": round(file_size_mb, 2),
                "tokens_per_mb": tokens_per_mb,
            }
            console.print(json.dumps(result, indent=2))
        else:
            console.print("\n[bold green]EPUB Token Analysis[/bold green]")
            console.print(f"File: [bold]{epub_path}[/bold]")
            console.print(f"Model: [bold]{model}[/bold]")
            console.print(f"Token count: [bold]{token_count:,}[/bold]")
            console.print(f"File size: [bold]{file_size:,}[/bold] bytes ([bold]{file_size_mb:.2f}[/bold] MB)")
            console.print(f"Tokens per MB: [bold]{tokens_per_mb:,}[/bold]")
            
            # Provide some context about costs if it's an OpenAI model
            if model.startswith("gpt"):
                # Very rough estimate based on current OpenAI pricing
                input_cost_per_1k = 0.01  # Assume lowest tier pricing (about $0.01/1K tokens)
                estimated_cost = (token_count / 1000) * input_cost_per_1k
                console.print(f"\n[italic]Estimated cost (input only): ${estimated_cost:.2f}[/italic]")
                console.print("[italic]Note: This is a rough estimate and actual costs may vary.[/italic]")
    
    except Exception as e:
        if ctx.obj and ctx.obj.get("DEBUG"):
            raise
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        return 1
