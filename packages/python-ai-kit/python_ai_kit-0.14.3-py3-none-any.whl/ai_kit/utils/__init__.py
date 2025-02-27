from typing import Dict, Any, AsyncIterable, Iterable, AsyncIterator
import logging as py_logging
import tiktoken
import re

# Import commonly used functions from submodules
from ai_kit.utils.logging import get_text, print_stream, rich_print_stream

logger = py_logging.getLogger(__name__)

def count_tokens(text: str, encoding_name: str = "cl100k_base") -> int:
    """Count the number of tokens in a string."""
    encoding = tiktoken.get_encoding(encoding_name)
    return len(encoding.encode(text))

def truncate_to_tokens(text: str, max_tokens: int, encoding_name: str = "cl100k_base") -> str:
    """
    Truncate text to a maximum number of tokens.
    
    Args:
        text: The text to truncate
        max_tokens: Maximum number of tokens to keep
        encoding_name: The name of the tiktoken encoding to use
        
    Returns:
        The truncated text as a string
    """
    encoding = tiktoken.get_encoding(encoding_name)
    tokens = encoding.encode(text)[:max_tokens]
    return encoding.decode(tokens)

def strip_ansi(text):
    """Remove ANSI escape sequences from text."""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)
