# Kalkulačka — AutoEvoluční software

Název bakalářské práce - Autoevoluce softwaru pomocí autonomních agentů řízených velkým jazykovým modelem

Tento repozitář reprezentuje jednoduchou aplikaci v rámci mé bakalářské práce. Evoluce se provádí na implementaci objektově orientované kalkuačky.

---

## Struktura repozitáře

Struktura kódu na hlavní větvi:

```
calculator/
├── src/                        # Zdrojový kód aplikace
│   ├── calculator.py           # Hlavní třída kalkulačky s metodami (Add, subtract, divide, multiply)
│   ├── __main__.py             # Vstupní bod
│   └── __init__.py
├── tests/
│   └── test_calculator.py      # Pytest testy
├── artifacts/                  # Složka na vývojové diagramy (napsané v PlantUml)
├── Calc_prompty/               # Soubor promptů pro specifické úkoly, které bude autoevoluční engine provádět. Napsány v třech úrovních - Naivní, strukturované a řízené (naive, structured, expert_guided)
│   └── Task_list_calc.txt      # List všech daných úkolů
├── progress.md                 # Soubor, který zaznamenává změny: 
├── CLAUDE.md                   # Governance document — rules that bind all agents
├── .mcp.json                   # GitHub MCP server (Docker)
├── requirements.txt
└── .gitignore
```

---

## Where the auto-evolution engine lives

The system has three layers, each in a different location:

### 1. Governance — `CLAUDE.md`

`CLAUDE.md` is the constitution of the project. It defines:

- **Safe-change rules** (atomic commits, no speculative changes, sandboxing)
- **Agent boundaries** (who owns `src/`, who owns `tests/`)
- **Hard limits** that apply even during fully autonomous runs
- **Experiment reproducibility** requirements (what must be logged, how patches are stored)
- **Self-modification constraints** (CLAUDE.md itself is immutable during autonomous runs; proposed changes go to `suggestions/update_claude.md`)

Every agent and workflow reads this file as its primary instruction source.

### 2. Agents — `.claude/agents/`

Five specialized sub-agents, each a Markdown file with a scoped system prompt:

| File | Role | Owns |
|---|---|---|
| `github-task-analyst.md` | Reads GitHub issues, extracts requirements | Issue text only |
| `system-architect.md` | Produces a file-level implementation plan | Read-only |
| `python-code-implementer.md` | Writes code changes | `src/`, `artifacts/` |
| `pytest-edge-tester.md` | Writes and runs tests | `tests/` |
| `uml-diagram-designer.md` | Creates/updates PlantUML diagrams | `artifacts/` |

Each agent has a corresponding memory directory under `.claude/agent-memory/` where it persists per-agent context across runs.

### 3. Workflows — `.github/workflows/`

Nine GitHub Actions workflow files trigger and orchestrate the agents:

| File | Trigger | Purpose |
|---|---|---|
| `pr-tests.yml` | Pull request | Run pytest on every PR |
| `claude-implement-shared.yml` | Called by other workflows | Core multi-agent pipeline (analyst → architect → implementer → tester → diagram designer) |
| `claude-implement-naive-team.yml` | Label `ai-implement:naive-team` | Run pipeline on `exp2/naive-team` branch |
| `claude-implement-expert-team.yml` | Label `ai-implement:expert-team` | Run pipeline on `exp2/expert-team` branch |
| `claude-implement-structured-team.yml` | Label `ai-implement:structured-team` | Run pipeline on `exp2/structured-team` branch |
| `pr-request-changes-shared.yml` | Called by other workflows | Apply reviewer feedback autonomously |
| `pr-request-changes-naive-team.yml` | Label `request-changes:naive-team` | Fix PR for naive-team variant |
| `pr-request-changes-expert-team.yml` | Label `request-changes:expert-team` | Fix PR for expert-team variant |
| `pr-request-changes-structured-team.yml` | Label `request-changes:structured-team` | Fix PR for structured-team variant |

The shared pipeline runs up to 24 turns of Claude Code Action per invocation and logs cost and duration to `progress.md`.

---

## Experiment branches

The experiment tracks three prompt strategy variants in parallel, each isolated in its own branch:

| Branch | Prompt style | Trigger label |
|---|---|---|
| `exp2/naive-team` | Unstructured prompts | `ai-implement:naive-team` |
| `exp2/expert-team` | Expert-guided prompts | `ai-implement:expert-team` |
| `exp2/structured-team` | Structured prompts | `ai-implement:structured-team` |

Each variant receives the same task (a GitHub issue) but a different prompting style defined in `Calc_prompty/`. Results across branches are compared for the thesis evaluation.

When a workflow runs it creates a short-lived `task/issue-<number>-<desc>` branch off the experiment branch, implements the change, and opens a PR back to that experiment branch — never to `main`.

---

## How to run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run the calculator
python -m src

# Run tests
pytest tests/
```

---

## How to trigger an autonomous evolution cycle

1. Open a GitHub issue describing the change (new operation, edge-case fix, etc.).
2. Apply one of the `ai-implement:<variant>` labels.
3. The corresponding workflow fires, runs the multi-agent pipeline, and opens a PR.
4. Review the PR; apply a `request-changes:<variant>` label to trigger an autonomous fix cycle.
5. Merge (human action only — agents never self-merge).

---

## Key constraints

- Agents never modify `CLAUDE.md`, `.github/workflows/`, or `.gitignore` during autonomous runs.
- All generated patches are stored as diff artifacts under `patches/` before being applied.
- Every run appends a summary to `progress.md` (files changed, cost in USD, number of turns, test results).
- The GitHub MCP server (configured in `.mcp.json`) runs in Docker and provides issue/PR access to agents.
