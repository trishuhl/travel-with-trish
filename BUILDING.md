# How I Built This

This project was an explicit experiment in AI-assisted development. Here's what actually happened.

## The problem

I kept Googling weather for trips and still packing wrong. Generic packing list apps give you the same list for Lisbon in June and Reykjavik in October. I wanted something that read the actual forecast and made actual decisions.

## The approach

I used two AI tools deliberately, for different things.

### Claude Code — architecture and integration

Claude Code handled the parts that required holding the whole system in mind at once:

- **Project scaffolding** — I described what I wanted and it laid out the file structure. `pack.py`, `weather.py`, `prompt.py`, `display.py`, `saver.py`. Each with a clear job.
- **Weather API integration** — The Open-Meteo geocoding + forecast pipeline, date parsing, WMO weather code mapping. I didn't want to figure out the API shape myself.
- **Prompt engineering iteration** — This took the most back-and-forth. Early versions returned generic lists. The breakthrough was being explicit in the prompt: *be specific and opinionated*, *add parenthetical notes where genuinely useful*, *do not pad the list*. That's what got "comfortable walking shoes ← cobblestones are no joke" instead of "shoes".

### GitHub Copilot — inline fill-in

Copilot filled gaps while I was already in the code:

- Click flag setup in `pack.py`
- The `_slugify` helper in `saver.py`
- Rich formatting boilerplate in `display.py`

These are the kinds of things where I knew exactly what I wanted but didn't want to type it out.

## What I learned

**The prompt is the product.** The weather API integration took an hour. Getting Claude to generate lists that felt genuinely useful — not padded, not generic — took longer. The system prompt in `prompt.py` went through probably six iterations.

**File structure is load-bearing.** Keeping `prompt.py` separate from `pack.py` made it easy to iterate on the prompt without touching anything else. Claude Code suggested this split. It was right.

**AI tools have different shapes.** Claude Code is good at "here's the system, build the pieces." Copilot is good at "I know what this line should be, just finish it." I used both, for different things, and it worked better than using either alone.

## What's next

See the README. The `--remember` flag and multi-city support are the ones I actually want.
