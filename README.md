# Calculator — Bachelor Thesis Project

A modular Python calculator with CLI and interactive modes, developed as part of a bachelor thesis on self-evolving software.

---

## Installation

**Requirements:** Python 3.12 or later.

```bash
# Clone the repository
git clone <repo-url>
cd Calculator_bachelor_autoevolution_team

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate      # Linux / macOS
.venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt
```

---

## Quick Start

### CLI mode — evaluate a one-shot expression

```bash
python -m src "3 + 4"          # 7
python -m src "2 ** 10 / 8"    # 128.0
python -m src "(5 + 3) * 2"    # 16
```

Supported operators: `+`, `-`, `*`, `/`, `**`. Parentheses and unary minus are also supported.

### Interactive mode — menu-driven prompt

```bash
python -m src
```

Select an operation by name (`add`, `subtract`, `multiply`, `divide`, `factorial`, `square`, `cube`, `square_root`, `cube_root`, `power`, `log10`, `natural_log`), enter the operand(s), and read the result. Type `quit` or `exit` to leave.

---

## Documentation

| Document | Description |
|---|---|
| [docs/README.md](docs/README.md) | Documentation index and quick-start |
| [docs/USER_GUIDE.md](docs/USER_GUIDE.md) | Full CLI and interactive usage guide with examples |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Module breakdown, data flow, and design patterns |
| [docs/API_REFERENCE.md](docs/API_REFERENCE.md) | Complete API reference for programmatic use |
| [docs/EXTENDING.md](docs/EXTENDING.md) | How to add new operations and presentation modes |