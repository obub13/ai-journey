# Graph Report - .  (2026-07-07)

## Corpus Check
- Corpus is ~8,554 words - fits in a single context window. You may not need a graph.

## Summary
- 80 nodes · 87 edges · 17 communities (15 shown, 2 thin omitted)
- Extraction: 76% EXTRACTED · 24% INFERRED · 0% AMBIGUOUS · INFERRED: 21 edges (avg confidence: 0.84)
- Token cost: 73,365 input · 0 output

## Community Hubs (Navigation)
- Ticket Triage Automation Scripts
- TriageAI Web UI & Rationale
- Stock Analysis Data Models
- TriageAI Tech Stack Decisions
- Graphify Tool Commands
- Alpaca Stock News Adapter
- Requests Dependency

## God Nodes (most connected - your core abstractions)
1. `AI-journey Repository Purpose` - 11 edges
2. `Anthropic Claude API` - 10 edges
3. `graphify knowledge graph tool` - 8 edges
4. `TriageAI project` - 8 edges
5. `TriageAI tech stack` - 6 edges
6. `claude_weather.py (weather-based Claude prompts)` - 5 edges
7. `daily_brief.py (daily brief generation)` - 5 edges
8. `index.html - Support Ticket Analyzer template` - 5 edges
9. `script.py (classifies tickets.json with Claude)` - 4 edges
10. `history.html - Ticket History template` - 4 edges

## Surprising Connections (you probably didn't know these)
- `Ticket History page screenshot (Hebrew tickets with urgency/issue badges)` --semantically_similar_to--> `history.html - Ticket History template`  [INFERRED] [semantically similar]
  screenshots/history.png → ticket-triage/templates/history.html
- `Analyzer page screenshot (TriageAI analyze view with Hebrew ticket + analysis result)` --semantically_similar_to--> `index.html - Support Ticket Analyzer template`  [INFERRED] [semantically similar]
  screenshots/analyzer.png → ticket-triage/templates/index.html
- `Structured daily learning habit rationale for the repo` --semantically_similar_to--> `AI-journey Repository Purpose`  [INFERRED] [semantically similar]
  README.md → AGENTS.md
- `python-dotenv dependency` --semantically_similar_to--> `AI-journey Repository Purpose`  [INFERRED] [semantically similar]
  ticket-triage/requirements.txt → AGENTS.md
- `ticket_triage.py (paste-ticket analysis script)` --semantically_similar_to--> `TriageAI project`  [INFERRED] [semantically similar]
  AGENTS.md → README.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **TriageAI Flask Web Application** — readme_triageai, ticket_triage_templates_index_page, ticket_triage_templates_history_page, ticket_triage_requirements_flask, ticket_triage_requirements_anthropic, ticket_triage_requirements_supabase [INFERRED 0.85]
- **Repo scripts using the Anthropic Claude API** — support_agent_module, ticket_triage_module, script_module, claude_classifier_module, claude_weather_module, daily_brief_module, anthropic_claude_api [INFERRED 0.85]
- **TriageAI Technical Decisions Rationale Set** — readme_claude_haiku_decision, readme_supabase_decision, readme_flask_decision, readme_render_decision [EXTRACTED 1.00]

## Communities (17 total, 2 thin omitted)

### Community 0 - "Ticket Triage Automation Scripts"
Cohesion: 0.17
Nodes (18): Agent editing guidance: prefer small incremental changes, preserve procedural style, CLAUDE_API_KEY environment variable, OPENWEATHER_API_KEY environment variable, AI-journey Repository Purpose, Anthropic Claude API, claude_classifier.py (ticket classification workflow), claude_weather.py (weather-based Claude prompts), daily_brief.py (daily brief generation) (+10 more)

### Community 1 - "TriageAI Web UI & Rationale"
Cohesion: 0.20
Nodes (14): TriageAI features list, Design limitation: kept as triage tool (not full resolution agent) since no system docs are given to Claude, Structured daily learning habit rationale for the repo, TriageAI project, Rationale: built to automate ticket triage for own support job, Analyzer page screenshot (TriageAI analyze view with Hebrew ticket + analysis result), Ticket History page screenshot (Hebrew tickets with urgency/issue badges), Urgency/status badge CSS system (High/Medium/Low, New/In Progress/Resolved) (+6 more)

### Community 2 - "Stock Analysis Data Models"
Cohesion: 0.27
Nodes (6): get_quote(), Fetches the quote data for a given stock symbol from the Finnhub API.      Arg, get_time_series(), Fetches the time series data for a given stock symbol from the Twelve Data API., PriceCandle, StockQuote

### Community 3 - "TriageAI Tech Stack Decisions"
Cohesion: 0.20
Nodes (10): Flask framework, Decision: Flask for lightweight, minimal-setup web framework, Make.com automation, Render hosting platform, Decision: Render for free hosting with auto GitHub deploys, Supabase (PostgreSQL), Decision: Supabase for free persistent PostgreSQL storage, TriageAI tech stack (+2 more)

### Community 4 - "Graphify Tool Commands"
Cohesion: 0.25
Nodes (8): graphify explain command, graphify-out/graph.json, graphify-out/GRAPH_REPORT.md, graphify knowledge graph tool, graphify path command, graphify query command, graphify update command (AST-only, no API cost), graphify-out/wiki/index.md

## Knowledge Gaps
- **19 isolated node(s):** `project.py (empty placeholder)`, `CLAUDE_API_KEY environment variable`, `OPENWEATHER_API_KEY environment variable`, `graphify-out/graph.json`, `graphify-out/GRAPH_REPORT.md` (+14 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `AI-journey Repository Purpose` connect `Ticket Triage Automation Scripts` to `TriageAI Web UI & Rationale`, `Graphify Tool Commands`?**
  _High betweenness centrality (0.169) - this node is a cross-community bridge._
- **Why does `TriageAI project` connect `TriageAI Web UI & Rationale` to `Ticket Triage Automation Scripts`, `TriageAI Tech Stack Decisions`?**
  _High betweenness centrality (0.148) - this node is a cross-community bridge._
- **Why does `TriageAI tech stack` connect `TriageAI Tech Stack Decisions` to `Ticket Triage Automation Scripts`, `TriageAI Web UI & Rationale`?**
  _High betweenness centrality (0.140) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `AI-journey Repository Purpose` (e.g. with `graphify knowledge graph tool` and `Structured daily learning habit rationale for the repo`) actually correct?**
  _`AI-journey Repository Purpose` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Fetches the latest news for a given stock symbol from the Alpaca API.      Arg`, `Fetches the quote data for a given stock symbol from the Finnhub API.      Arg`, `Fetches the time series data for a given stock symbol from the Twelve Data API.` to the rest of the system?**
  _29 weakly-connected nodes found - possible documentation gaps or missing edges._