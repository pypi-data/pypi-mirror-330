import logging
import click
from typing import Optional
from ai_kit.config.client_config import ClientFactory
from ai_kit.cli.registry import registry_instance
from ai_kit.shared_console import shared_console, shared_error_console
from time import perf_counter
from ai_kit.core.prompt_loader import PromptLoader
from ai_kit.utils.fs import load_system_prompt, package_root
from ai_kit.utils.logging import rich_print_stream
import asyncio

logger = logging.getLogger(__name__)

# Get package root and load Clyde's system prompt
PACKAGE_ROOT = package_root()
CLYDE_PROMPT_PATH = f"{PACKAGE_ROOT}/system_prompts/teammates/clyde.md"

# Teammate color - light blue (Deep Sky Blue) for all teammates
TEAMMATE_COLOR = "#00BFFF"  # Deep Sky Blue hex color

async def clyde_command(
    query: str,
    system_prompt: Optional[str] = None,
    model: str = "r1",
    use_mock: bool = True,  # For demo purposes
):
    """
    Implementation of the Clyde teammate command.

    Args:
        query: The query to send to Clyde
        system_prompt: The system prompt to use (if None, loads from file)
        model: The model to use
        use_mock: Whether to use a mock stream for demonstration (default: True)
    """
    s = perf_counter()

    # Load the system prompt if not provided
    if system_prompt is None:
        try:
            system_prompt = load_system_prompt(CLYDE_PROMPT_PATH)
        except Exception as e:
            shared_error_console.print(f"[bold red]Error loading Clyde system prompt:[/] {str(e)}")
            logger.error(f"Error loading Clyde system prompt: {str(e)}", exc_info=True)
            return ""

    # Process the query with PromptLoader to handle any file/URL references
    try:
        prompt_loader = PromptLoader()
        processed_query = await prompt_loader.load(query)
    except Exception as e:
        shared_error_console.print(f"[bold red]Error processing query:[/] {str(e)}")
        logger.error(f"Error in clyde_command: {str(e)}", exc_info=True)
        return ""

    try:
        if use_mock:
            # Debug test for color output 
            shared_console.print("\nDemonstrating colored output with mock stream:", style="yellow")
            
            # Create a simple async generator that yields chunks
            async def mock_stream():
                yield {"choices": [{"delta": {"content": "Clyde here. "}}]}
                await asyncio.sleep(0.2)
                yield {"choices": [{"delta": {"content": "When asking if simplicity is better than complexity, "}}]}
                await asyncio.sleep(0.2)
                yield {"choices": [{"delta": {"content": "I wonder: "}}]}
                await asyncio.sleep(0.2)
                yield {"choices": [{"delta": {"content": "\n\n- What problem are you solving? "}}]}
                await asyncio.sleep(0.2)
                yield {"choices": [{"delta": {"content": "\n- Who needs to understand and maintain your solution? "}}]}
                await asyncio.sleep(0.2)
                yield {"choices": [{"delta": {"content": "\n- Will this solution need to adapt to future changes? "}}]}
                await asyncio.sleep(0.2)
                yield {"choices": [{"delta": {"content": "\n\nSimplicity serves users and maintainers. Complexity often serves edge cases. "}}]}
                await asyncio.sleep(0.2)
                yield {"choices": [{"delta": {"content": "Which matters more for your specific needs?"}}]}
            
            # Print the mock stream in teammate color
            response = await rich_print_stream(mock_stream(), style=TEAMMATE_COLOR)
        else:
            with shared_console.status("[bold green]Thinking...[/bold green]"):
                try:
                    # Get the client for the specified model
                    client = ClientFactory.get_client_by_model(model)

                    # Set up the message content
                    messages = [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": processed_query},
                    ]

                    # Call the model and stream the response
                    response_stream = await client.chat_completion(
                        messages=messages, stream=True
                    )

                    # Print the stream in teammate color and store the final response
                    response = await rich_print_stream(response_stream, style=TEAMMATE_COLOR)

                except Exception as e:
                    shared_error_console.print(
                        f"[bold red]Error calling Clyde:[/] {str(e)}"
                    )
                    logger.error(f"Error in clyde_command: {str(e)}", exc_info=True)
                    return ""

        e = perf_counter()
        shared_console.print(
            f"\n[yellow]Response generated in {e - s:0.2f} seconds.[/yellow]\n"
        )

        return response

    except Exception as e:
        shared_error_console.print(f"[bold red]Error:[/] {str(e)}")
        logger.error(f"Error in clyde_command: {str(e)}", exc_info=True)
        return ""
