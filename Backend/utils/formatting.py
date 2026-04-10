def format_currency(value: float) -> str:
    """Format a number as currency"""
    return f"${value:,.2f}"


def format_percentage(value: float) -> str:
    """Format a number as percentage"""
    return f"{value:.2f}%"
