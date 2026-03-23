import click
import os
import sys
from weather import get_forecast
from prompt import build_prompt
from display import print_packing_list
from saver import save_list
import anthropic


@click.command()
@click.option("--to", "destination", required=True, help="Destination (city, country)")
@click.option("--dates", required=True, help='Travel dates e.g. "June 10-17" or "June 10-17, 2025"')
@click.option(
    "--style",
    default="casual",
    type=click.Choice(["casual", "adventure", "business", "beach"]),
    show_default=True,
    help="Travel style",
)
@click.option("--save", "do_save", is_flag=True, default=False, help="Save list to markdown file")
@click.option("--output", default=None, help="Custom save path (implies --save)")
def main(destination, dates, style, do_save, output):
    """Generate a weather-aware packing list for your trip."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        click.echo("Error: ANTHROPIC_API_KEY environment variable not set.", err=True)
        sys.exit(1)

    click.echo(f"📍 Looking up weather for {destination}...")
    try:
        forecast = get_forecast(destination, dates)
    except Exception as e:
        click.echo(f"Error fetching weather: {e}", err=True)
        sys.exit(1)

    click.echo("🤖 Asking Claude to build your packing list...")
    prompt = build_prompt(destination, dates, forecast, style)

    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    response = message.content[0].text

    print_packing_list(destination, dates, forecast, response)

    if output or do_save:
        path = save_list(destination, dates, forecast, response, output)
        click.echo(f"\n✅ Saved to {path}")


if __name__ == "__main__":
    main()
