from rich.console import Console
from rich.rule import Rule
from rich.text import Text
from rich.padding import Padding

console = Console()


def print_packing_list(destination: str, dates: str, forecast: dict, response: str) -> None:
    """Print the packing list with a rich header and formatted body."""
    console.print()
    console.print(Rule(style="dim"))

    # Header
    title = Text(f"🧳 Packing List — {forecast['destination']}", style="bold")
    console.print(Padding(title, (0, 1)))

    conditions = ", ".join(forecast["conditions"]) if forecast["conditions"] else "Mixed"
    weather_line = (
        f"   Highs {forecast['temp_max_c']}°C · "
        f"Lows {forecast['temp_min_c']}°C · "
        f"{conditions} · "
        f"{forecast['max_precip_pct']}% rain chance"
    )
    console.print(Text(weather_line, style="dim"))
    console.print(Rule(style="dim"))
    console.print()

    # Body — print Claude's response line by line with light formatting
    for line in response.strip().splitlines():
        stripped = line.strip()
        if not stripped:
            console.print()
            continue

        # Category headers (lines starting with an emoji category marker)
        if stripped and stripped[0] in "👕🧴🔌🎒" and len(stripped) < 60:
            console.print(Text(f"\n{stripped}", style="bold yellow"))
        # Summary line
        elif stripped.startswith("✅"):
            console.print()
            console.print(Rule(style="dim"))
            console.print(Text(stripped, style="bold green"))
        # Bullet items
        elif stripped.startswith("•") or stripped.startswith("-"):
            console.print(Text(f"  {stripped}", style="white"))
        else:
            console.print(Text(f"  {stripped}", style="white"))

    console.print()
