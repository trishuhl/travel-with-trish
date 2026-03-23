import os
import re
from pathlib import Path
from datetime import date


def save_list(
    destination: str,
    dates: str,
    forecast: dict,
    response: str,
    output: str | None = None,
) -> str:
    """Save the packing list as a markdown file. Returns the path saved to."""
    if output:
        path = Path(output).expanduser()
    else:
        slug = _slugify(forecast["destination"])
        date_slug = date.today().strftime("%Y-%m")
        filename = f"{slug}-{date_slug}.md"
        save_dir = Path.home() / "packing-lists"
        save_dir.mkdir(parents=True, exist_ok=True)
        path = save_dir / filename

    conditions = ", ".join(forecast["conditions"]) if forecast["conditions"] else "Mixed"
    header = f"""# 🧳 Packing List — {forecast['destination']}

**Dates:** {dates} ({forecast['start']} to {forecast['end']})
**Weather:** Highs {forecast['temp_max_c']}°C · Lows {forecast['temp_min_c']}°C · {conditions} · {forecast['max_precip_pct']}% rain chance

---

"""

    path.write_text(header + response.strip() + "\n", encoding="utf-8")
    return str(path)


def _slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = text.strip("-")
    return text
