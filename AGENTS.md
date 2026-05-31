# AI Agent Instructions for AI-journey

## Repository purpose
This repository is a personal Python AI experiment collection. It contains small standalone scripts that call Anthropic Claude and OpenWeather APIs for support ticket processing, classification, daily briefs, and weather summary tasks.

## Key files
- `support_agent.py` – interactive support ticket responder using Claude with follow-up question handling.
- `ticket_triage.py` – analyzes a pasted support ticket and returns structured ticket metadata plus a draft reply.
- `script.py` – classifies tickets in `tickets/tickets.json` with Claude and writes categories back to the file.
- `claude_classifier.py` – another ticket-classification workflow using Claude.
- `claude_weather.py` / `daily_brief.py` – weather-based Claude prompts and daily brief generation.
- `project.py` – currently empty placeholder.

## Environment and runtime
- This is not a packaged Python project. Run scripts directly with the workspace Python interpreter.
- Uses `.env` for secrets via `python-dotenv`.
- Required environment variables:
  - `CLAUDE_API_KEY`
  - `OPENWEATHER_API_KEY` (for weather-related scripts)

## Agent guidance
- Prefer small incremental changes to these scripts rather than introducing large frameworks or packaging.
- Preserve the existing procedural style and interactive prompt patterns.
- When editing support-ticket logic, keep responses structured and respect the current Claude system prompt rules.
- Avoid assuming a web server, database, or external build/test tooling exists.

## Notes for future customization
- There is currently no `.github/copilot-instructions.md` or other agent customization file.
- If the project grows, consider splitting instructions into a dedicated `.github/copilot-instructions.md` for general repo behavior and a second `AGENTS.md` for AI task-specific guidance.
