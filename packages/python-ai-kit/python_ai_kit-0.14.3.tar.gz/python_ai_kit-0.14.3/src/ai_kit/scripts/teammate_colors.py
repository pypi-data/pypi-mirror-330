#!/usr/bin/env python
"""
Teammate Colors Demo Script

This script demonstrates various color options for AI-Kit teammates,
including standard colors, named colors, blue shades, and hex colors.
It also shows how different teammates can be displayed with different colors.
"""
import asyncio
import argparse
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

# Import from ai_kit if available
try:
    from ai_kit.shared_console import shared_console
    from ai_kit.utils.logging import rich_print_stream
    AI_KIT_AVAILABLE = True
except ImportError:
    # Fallback for standalone use
    AI_KIT_AVAILABLE = False

# Create a console for rich output
console = Console()

# Standard colors that work in most Rich installations
STANDARD_COLORS = [
    "red", "green", "blue", "yellow", "magenta", "cyan", "white", 
    "bright_red", "bright_green", "bright_blue", "bright_yellow", 
    "bright_magenta", "bright_cyan", "bright_white"
]

# Named colors from the extended set that are commonly available
NAMED_COLORS = [
    "purple", "orange", "pink", "gold", "violet", 
    "turquoise", "salmon", "plum", "orchid", "indigo",
    "lime", "maroon", "navy", "olive", "teal"
]

# Blue/Cyan colors commonly available
BLUE_SHADES = [
    "blue", "bright_blue", "cyan", "bright_cyan", 
    "turquoise", "navy", "teal", "royal_blue",
    "dodger_blue", "steel_blue", "sky_blue"
]

# Define teammate color options with hex values for precise control
BLUE_HEX_OPTIONS = [
    ("#00BFFF", "Deep Sky Blue - Good for technical teammates"),
    ("#1E90FF", "Dodger Blue - Good for analytical teammates"),
    ("#87CEEB", "Sky Blue - Good for supportive teammates"),
    ("#4682B4", "Steel Blue - Good for strategic teammates"),
    ("#6495ED", "Cornflower Blue - Good for creative teammates"),
]

GREEN_HEX_OPTIONS = [
    ("#32CD32", "Lime Green - Good for growth-focused teammates"),
    ("#3CB371", "Medium Sea Green - Good for balanced teammates"),
    ("#2E8B57", "Sea Green - Good for grounding teammates"),
    ("#00FA9A", "Medium Spring Green - Good for innovative teammates"),
    ("#66CDAA", "Medium Aquamarine - Good for calm teammates"),
]

OTHER_HEX_OPTIONS = [
    ("#9370DB", "Medium Purple - Good for imaginative teammates"),
    ("#FF6347", "Tomato - Good for critical teammates"),
    ("#FFD700", "Gold - Good for optimistic teammates"),
    ("#FF69B4", "Hot Pink - Good for energetic teammates"),
    ("#8A2BE2", "Blue Violet - Good for visionary teammates"),
]

# Define different teammate examples
TEAMMATE_COLORS = {
    "clyde": "#00BFFF",      # Deep Sky Blue (current Clyde color)
    "sage": "green",         # Example: Sage in green
    "aurora": "bright_blue", # Example: Aurora in bright blue
    "mercury": "yellow",     # Example: Mercury in yellow
    "nova": "magenta",       # Example: Nova in magenta
}

async def demo_standard_colors():
    """Display a demo of standard Rich colors."""
    console.print(Panel("Standard Colors", style="bold"))
    for color in STANDARD_COLORS:
        text = Text(f"This is text in {color} color")
        text.stylize(color)
        console.print(text)
    
    console.print("\n")
    
    # Show named colors
    console.print(Panel("Named Colors", style="bold"))
    for color in NAMED_COLORS:
        try:
            text = Text(f"This is text in {color} color")
            text.stylize(color)
            console.print(text)
        except Exception:
            # Skip colors that aren't available
            pass
    
    console.print("\n")
    
    # Show blue shades
    console.print(Panel("Blue Shades (Good for Teammates)", style="bold"))
    for color in BLUE_SHADES:
        try:
            text = Text(f"This is text in {color} color")
            text.stylize(color)
            console.print(text)
        except Exception:
            # Skip colors that aren't available
            pass
    
    # Show other color formats
    console.print(Panel("RGB and Hex Colors", style="bold"))
    console.print(Text("RGB color (0,128,255)", style="rgb(0,128,255)"))
    console.print(Text("Hex color #00BFFF (deep sky blue)", style="#00BFFF"))
    console.print(Text("Hex color #1E90FF (dodger blue)", style="#1E90FF"))
    console.print(Text("Hex color #87CEEB (sky blue)", style="#87CEEB"))
    console.print(Text("Hex color #00FFFF (cyan/aqua)", style="#00FFFF"))
    
    # Special note about Clyde's current color
    console.print("\n")
    console.print(Panel("Current Teammate Settings", style="bold"))
    console.print(Text("Clyde currently uses Deep Sky Blue (#00BFFF)", style="#00BFFF"))

def demo_color_row(console, hex_color, description):
    """Display a row with sample text in the given hex color."""
    console.print(f"[{hex_color}]████████████████████████████████████[/]  ", end="")
    console.print(f"[{hex_color}]This text is colored with {hex_color}[/]  ", end="")
    console.print(f"- {description}")

async def demo_hex_colors():
    """Run the hex color demonstration for teammates."""
    console.print(Panel.fit(
        "Hex Color Options for Teammates", 
        style="bold white on blue"
    ))
    
    console.print("\n[bold]Blue Color Options:[/bold]")
    for hex_color, description in BLUE_HEX_OPTIONS:
        demo_color_row(console, hex_color, description)
    
    console.print("\n[bold]Green Color Options:[/bold]")
    for hex_color, description in GREEN_HEX_OPTIONS:
        demo_color_row(console, hex_color, description)
    
    console.print("\n[bold]Other Color Options:[/bold]")
    for hex_color, description in OTHER_HEX_OPTIONS:
        demo_color_row(console, hex_color, description)
    
    console.print("\n[bold]Currently Implemented:[/bold]")
    console.print("[#00BFFF]Clyde currently uses Deep Sky Blue (#00BFFF) which appears like this[/#00BFFF]")
    console.print("To update the color, modify the TEAMMATE_COLOR constant in src/ai_kit/cli/teammates/clyde.py:")
    console.print("TEAMMATE_COLOR = \"#00BFFF\"  # Deep Sky Blue")
    
    console.print("\n[bold]Recommendation for Light Blue:[/bold]")
    console.print("[#00BFFF]If you want a light blue color, #00BFFF (Deep Sky Blue) is a good choice[/#00BFFF]")
    console.print("[#1E90FF]Or #1E90FF (Dodger Blue) for a slightly deeper blue[/#1E90FF]")

async def mock_stream(teammate_name, message):
    """Create a mock stream with a teammate's response."""
    # Simulate the structure of AI response chunks
    yield {"choices": [{"delta": {"content": f"{teammate_name.capitalize()} here. "}}]}
    await asyncio.sleep(0.2)
    
    # Split the message into chunks to simulate streaming
    words = message.split()
    buffer = []
    for word in words:
        buffer.append(word)
        if len(buffer) >= 3 or word.endswith(('.', '!', '?')):
            yield {"choices": [{"delta": {"content": " ".join(buffer) + " "}}]}
            buffer = []
            await asyncio.sleep(0.1)
    
    # Send any remaining words
    if buffer:
        yield {"choices": [{"delta": {"content": " ".join(buffer)}}]}

async def demo_teammates():
    """Demonstrate how different teammates would appear with different colors."""
    console.print("\n[bold]Demonstration of Teammate Colors in AI-Kit[/bold]\n")
    
    for teammate, color in TEAMMATE_COLORS.items():
        console.print(f"\n[bold]{teammate.capitalize()} (using color '{color}'):[/bold]")
        
        # Create an appropriate message for each teammate
        if teammate == "clyde":
            message = "I'll challenge unnecessary complexity. Is that feature really worth the engineering time?"
        elif teammate == "sage":
            message = "Let me share some wisdom about your project architecture. Have you considered breaking this down into smaller components?"
        elif teammate == "aurora":
            message = "I notice patterns in your code that could be streamlined. The algorithm could be optimized for better performance."
        elif teammate == "mercury":
            message = "Working at speed! Let's rapidly prototype this solution and get feedback before investing more time."
        elif teammate == "nova":
            message = "Here's a creative approach to solving your problem. What if we looked at it from an entirely different perspective?"
        
        # Generate and print the teammate's response with appropriate color
        if AI_KIT_AVAILABLE:
            stream = mock_stream(teammate, message)
            await rich_print_stream(stream, style=color)
        else:
            # Fallback if rich_print_stream is not available
            console.print(f"{teammate.capitalize()} here. {message}", style=color)
        
        print()  # Add a newline after each teammate's response

async def main():
    """Run the color demonstration based on command line arguments."""
    parser = argparse.ArgumentParser(description="Teammate Color Demonstrations")
    parser.add_argument("--standard", action="store_true", help="Show standard colors")
    parser.add_argument("--hex", action="store_true", help="Show hex color options")
    parser.add_argument("--teammates", action="store_true", help="Show teammate examples")
    parser.add_argument("--all", action="store_true", help="Show all demonstrations")
    args = parser.parse_args()
    
    # If no specific arguments are provided, show all demos
    if not (args.standard or args.hex or args.teammates or args.all):
        args.all = True
    
    if args.all or args.standard:
        await demo_standard_colors()
        print("\n" + "-" * 80 + "\n")
    
    if args.all or args.hex:
        await demo_hex_colors()
        print("\n" + "-" * 80 + "\n")
    
    if args.all or args.teammates:
        if not AI_KIT_AVAILABLE and (args.teammates or args.all):
            console.print("\n[yellow]Note: Full teammate demonstration requires the AI-Kit environment.[/yellow]")
            console.print("[yellow]Falling back to a simplified version for demonstration purposes.[/yellow]\n")
        
        await demo_teammates()

if __name__ == "__main__":
    asyncio.run(main()) 