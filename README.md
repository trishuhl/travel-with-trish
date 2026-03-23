# 🧳 my-packing-list-cli
I got tired of Googling weather forecasts and still forgetting my umbrella. So I built this.
Give it a destination and dates — it pulls the actual forecast and asks Claude to generate a packing list tailored to *those specific conditions*. Not a generic template. A real list, for that trip.
```bash
pack --to "Lisbon, Portugal" --dates "June 10-17"
```
```
🧳 Packing List — Lisbon, Portugal (June 10–17)
   Highs 27–29°C · Lows 17°C · Mostly sunny · 10% rain
👕 Clothing
  • 4x lightweight t-shirts
  • 1x light linen shirt (evenings out)
  • 2x shorts
  • 1x chinos (versatile for dinners)
  • 1x light rain jacket (just in case)
  • Comfortable walking shoes ← cobblestones are no joke
  • 1x sandals
🧴 Toiletries
  • High SPF sunscreen (it's sunnier than you expect)
  • Lip balm with SPF
  • Reusable water bottle
🔌 Tech & Documents
  • EU power adapter (Type F)
  • Portable charger
  • Passport + digital backup
  • Travel insurance info
✅ 23 items · Saved to ~/packing-lists/lisbon-june-2025.md
```
---
## How it works
1. **Geocodes** your destination using [Open-Meteo's geocoding API](https://open-meteo.com/en/docs/geocoding-api)
2. **Fetches** the weather forecast for your travel dates (also Open-Meteo — free, no key needed)
3. **Builds** a prompt with location context + weather data and sends it to the [Claude API](https://anthropic.com)
4. **Prints** a clean, categorized list in the terminal via `rich`
5. **Optionally saves** the list as a markdown file
---
## Setup
```bash
git clone https://github.com/yourusername/my-packing-list-cli
cd my-packing-list-cli
pip install -r requirements.txt
```
Add your Anthropic API key:
```bash
export ANTHROPIC_API_KEY=your_key_here
```
Run it:
```bash
python pack.py --to "Tokyo, Japan" --dates "March 3-10"
```
---
## Options
| Flag | Description | Example |
|------|-------------|---------|
| `--to` | Destination (city, country) | `"Bangkok, Thailand"` |
| `--dates` | Travel dates | `"July 4-11"` or `"July 4-11, 2025"` |
| `--style` | Travel style (default: `casual`) | `adventure`, `business`, `beach` |
| `--save` | Save list to markdown file | `--save` |
| `--output` | Custom save path | `~/trips/tokyo.md` |
```bash
# Beach trip with auto-save
pack --to "Tulum, Mexico" --dates "Feb 14-21" --style beach --save
# Business travel
pack --to "Singapore" --dates "Sept 9-12" --style business
```
---
## Project structure
```
my-packing-list-cli/
├── pack.py               # CLI entrypoint (click)
├── weather.py            # Open-Meteo geocoding + forecast
├── prompt.py             # Claude prompt construction
├── display.py            # rich terminal output
├── saver.py              # markdown export
├── requirements.txt
├── .env.example
├── BUILDING.md           # how I built this with Claude Code + Copilot
└── README.md
```
---
## Tech stack
- **[Click](https://click.palletsprojects.com/)** — CLI flags and interface
- **[Open-Meteo](https://open-meteo.com/)** — weather + geocoding (free, no API key)
- **[Anthropic Python SDK](https://github.com/anthropic/anthropic-sdk-python)** — Claude API
- **[Rich](https://github.com/Textualize/rich)** — terminal formatting
---
## How I built this
This was built with AI-assisted coding as an explicit experiment — I wanted to understand how Claude Code and GitHub Copilot fit together in a real workflow.
**Claude Code** handled the heavy lifting upfront: scaffolding the project structure, writing the weather API integration end-to-end, and helping me iterate on the prompt until the packing lists felt genuinely useful rather than generic.
**GitHub Copilot** filled in the gaps inline: CLI flag setup, the markdown export function, and a lot of the `rich` formatting boilerplate.
The prompt engineering was mine. Getting Claude to say "comfortable walking shoes — cobblestones are no joke" instead of just "shoes" took a few iterations.
Full notes in [BUILDING.md](./BUILDING.md).
---
## What's next
- [ ] Multi-city trip support (`--stops "London, Paris, Barcelona"`)
- [ ] `--remember` flag to save your personal "always forget" items into every future list
- [ ] Trip history + diff: *"You packed this for Lisbon last time — want to reuse it?"*
- [ ] `--style adventure` / `--style beach` personas (partially done)
---
## Status
Works for me. May break for you. Issues and PRs welcome.
---
*Built by a PM who got tired of overpacking. Powered by [Claude](https://anthropic.com) and real weather data.*
