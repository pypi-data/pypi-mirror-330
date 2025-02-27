from typing import Union, List, Dict, Any, AsyncIterable
import logging
from ai_kit.shared_console import shared_console, shared_error_console

logger = logging.getLogger(__name__)

def get_text(chunk: Dict[str, Any]) -> str:
    """Get the text from a streaming chunk."""
    choices = chunk.get("choices")
    if not choices:
        shared_error_console.print(f"No choices found in chunk: {chunk}")
        return ""
    if not isinstance(choices, list):
        shared_error_console.print(f"Choices is not a list: {choices}")
        return ""
    
    delta = choices[0].get("delta")
    if not delta:
        shared_error_console.print(f"No delta found in choices: {choices}")
        return ""

    return delta.get("content") or delta.get("reasoning_content")

def get_headers(chunk: Dict[str, Any]) -> Dict[str, Any]:
    """Get the response headers from a streaming chunk."""
    if (h:=chunk.get("_response_headers")): return h
    return {}

async def rich_print_stream(chunks: AsyncIterable[Dict[str, Any]], buffer_size: int = 128, style: str = None) -> str:
    """
    Read text chunks from an async generator, print them to console with Rich formatting,
    and return the collected text.
    
    Args:
        chunks: Async iterable of chunks to process
        buffer_size: Size threshold for buffer before printing
        style: Rich style string to apply (color name or other Rich style)
        
    Returns:
        The complete text collected from all chunks
    """
    buffer = []  # We'll collect text pieces here
    current_size = 0
    output = ""

    async for chunk in chunks:
        text = get_text(chunk)
        if text:
            buffer.append(text)
            current_size += len(text)
            output += text
            # If we pass the threshold, print and reset
            if current_size >= buffer_size:
                if style:
                    shared_console.print("".join(buffer), style=style, end="", highlight=False)
                else:
                    shared_console.print("".join(buffer), end="", highlight=False)
                buffer = []
                current_size = 0

    if buffer:
        if style:
            shared_console.print("".join(buffer), style=style, end="", highlight=False)
        else:
            shared_console.print("".join(buffer), end="", highlight=False)

    return output

async def print_stream(chunks: AsyncIterable[Dict[str, Any]], buffer_size: int = 128) -> str:
    """
    Read text chunks from an async generator, print them to console as they arrive,
    and return the collected text.
    
    Args:
        chunks: Async iterable of chunks to process
        buffer_size: Size threshold for buffer before printing
        
    Returns:
        The complete text collected from all chunks
    """
    buffer = []  # We'll collect text pieces here
    current_size = 0
    output = ""

    async for chunk in chunks:
        text = get_text(chunk)
        if text:
            buffer.append(text)
            current_size += len(text)
            output += text
            # If we pass the threshold, print and reset
            if current_size >= buffer_size:
                print("".join(buffer), end="", flush=True)
                buffer = []
                current_size = 0

    if buffer:
        print("".join(buffer), end="", flush=True)

    return output