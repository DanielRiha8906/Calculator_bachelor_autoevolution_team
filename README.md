# Calculator

A Python command-line calculator supporting 12 mathematical operations with two interaction modes: an interactive REPL and a non-interactive CLI suitable for scripting.

## Documentation

- [User Guide](docs/USER_GUIDE.md) — installation, REPL and CLI usage, examples, error reference
- [Features](docs/FEATURES.md) — full operation catalog with definitions, aliases, and domain constraints
- [Project Structure](docs/PROJECT_STRUCTURE.md) — module overview, architecture, and data flow

## Quick Start

### Installation

```bash
python -m venv .venv
source .venv/bin/activate      # Linux / macOS
.venv\Scripts\activate         # Windows

pip install -r requirements.txt
```

### Usage

**Interactive REPL mode** (guided menu):

```bash
python -m src
```

**CLI mode** (single command, for scripting):

```bash
# Syntax: python -m src <operation> <operand1> [operand2]
python -m src add 3 4           # -> 7.0
python -m src sqrt 16           # -> 4.0
python -m src log 100 10        # -> 2.0
python -m src factorial 5       # -> 120
```

Supported operations: `add`, `subtract`, `multiply`, `divide`, `power`, `logarithm`, `factorial`, `square`, `cube`, `square_root`, `cube_root`, `natural_logarithm`.

Common aliases: `+`, `-`, `*`, `/`, `^`, `log`, `sqrt`, `cbrt`, `ln`.

See the [User Guide](docs/USER_GUIDE.md) for a complete list of examples and exit codes.

## Running Tests

```bash
python -m pytest tests/
```
