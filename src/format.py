def colored(text, color=None):
    """Auto-alternating color formatter between green/yellow.
    Args:
        text: Text to colorize
        color: Force specific color (None for auto-alternating)
    """
    if not hasattr(colored, "current_color"):
        colored.current_color = "green"  # Initialize

    # Use forced color if specified, else alternate
    use_color = color if color else colored.current_color

    colors = {"green": "\033[92m", "yellow": "\033[93m", "end": "\033[0m"}

    # Toggle color for next call (if not forced)
    if color is None:
        colored.current_color = (
            "yellow" if colored.current_color == "green" else "green"
        )

    return f"{colors[use_color]}{text}{colors['end']}"
