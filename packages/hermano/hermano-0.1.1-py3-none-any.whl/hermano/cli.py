#!/usr/bin/env python3
"""
Main CLI entry point for Hermano.
"""

import os
from pathlib import Path

import click
from dotenv import load_dotenv
from rich import print as rprint
from rich.console import Console

from hermano import __version__

# Initialize rich console for pretty output
console = Console()

# Load environment variables from .env file
env_path = Path.home() / ".env"
if env_path.exists():
    load_dotenv(env_path)

# Import command groups
from hermano.commands.epub_commands import epub


@click.group()
@click.version_option(version=__version__, prog_name="hermano")
@click.option("--debug", is_flag=True, help="Enable debug mode")
@click.pass_context
def cli(ctx, debug):
    """Hermano: LLM-powered Assistant for Operations.
    
    A CLI tool that leverages large language models to automate daily tasks.
    """
    # Ensure context object exists
    ctx.ensure_object(dict)
    ctx.obj["DEBUG"] = debug
    
    # Check for required API keys
    api_keys = {
        "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY"),
        "DEEPSEEK_API_KEY": os.environ.get("DEEPSEEK_API_KEY"),
        "GEMINI_API_KEY": os.environ.get("GEMINI_API_KEY"),
    }
    
    # Show warning if no API keys are set
    if not any(api_keys.values()) and not debug:
        rprint("[yellow]Warning:[/yellow] No API keys found. Some commands may not work.")
        rprint("[yellow]Set environment variables or create a .env file in your home directory.[/yellow]")


# Add command groups
cli.add_command(epub)


if __name__ == "__main__":
    cli()
