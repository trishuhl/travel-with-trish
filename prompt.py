def build_prompt(destination: str, dates: str, forecast: dict, style: str) -> str:
    """Build the Claude prompt from destination, dates, forecast, and travel style."""

    conditions = ", ".join(forecast["conditions"]) if forecast["conditions"] else "mixed"
    rain_note = ""
    if forecast["max_precip_pct"] >= 50:
        rain_note = f"There's a significant chance of rain (up to {forecast['max_precip_pct']}%)."
    elif forecast["max_precip_pct"] >= 20:
        rain_note = f"There's a small chance of rain (up to {forecast['max_precip_pct']}%), worth being prepared."

    style_notes = {
        "casual":    "This is a casual leisure trip — comfortable, versatile clothing.",
        "adventure": "This is an adventure/outdoor trip — pack for activity, durability, and variable conditions.",
        "business":  "This is a business trip — professional attire required, keep it streamlined.",
        "beach":     "This is a beach holiday — swimwear, sun protection, and light layers for evenings.",
    }

    prompt = f"""You are a practical, experienced travel packer. Generate a concise, specific packing list for this trip.

TRIP DETAILS:
- Destination: {forecast['destination']}
- Dates: {dates} ({forecast['start']} to {forecast['end']})
- Weather: Highs {forecast['temp_max_c']}°C / Lows {forecast['temp_min_c']}°C · {conditions}
- {rain_note}
- Style: {style_notes.get(style, style)}

RULES:
- Be specific and opinionated. Say "1x light linen shirt (evenings out)" not just "shirt".
- Add brief parenthetical notes where genuinely useful (e.g. "← cobblestones are no joke").
- Group items into categories: 👕 Clothing, 🧴 Toiletries, 🔌 Tech & Documents, 🎒 Extras.
- Tailor quantities to the trip length ({forecast['start']} to {forecast['end']}).
- Do not pad the list. Only include what's actually useful for these specific conditions.
- End with a single line: "✅ X items total" where X is the count of items across all categories.

Respond with only the packing list — no preamble, no sign-off.
"""
    return prompt
