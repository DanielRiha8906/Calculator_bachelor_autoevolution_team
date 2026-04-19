# Setup Guide

## Prerequisites

Python 3.12 is required. Verify your installation:

```
python3.12 --version
```

If `python3.12` is not available, install it via your system package manager
or from [python.org](https://www.python.org/downloads/).

---

## Creating a Virtual Environment

From the repository root, create a virtual environment using Python 3.12:

```
python3.12 -m venv .venv
```

---

## Activating the Virtual Environment

**Linux / macOS:**

```
source .venv/bin/activate
```

**Windows (Command Prompt):**

```
.venv\Scripts\activate.bat
```

**Windows (PowerShell):**

```
.venv\Scripts\Activate.ps1
```

After activation, your shell prompt will be prefixed with `(.venv)`.

---

## Installing Dependencies

With the virtual environment active, install the project dependencies:

```
pip install -r requirements.txt
```

If no `requirements.txt` is present (the project currently has no third-party
runtime dependencies), this step can be skipped. The application depends only
on the Python 3.12 standard library.

---

## Verification

Confirm everything is working by running the application in each mode.

**REPL mode** (interactive):

```
python -m src
```

You should see:

```
Welcome to the Calculator REPL. Type 'quit' to exit.
```

Type `quit` to exit immediately.

**CLI mode** (non-interactive):

```
python -m src add 2 3
```

Expected output:

```
5.0
```

---

## Deactivating the Virtual Environment

When you are finished, deactivate the environment:

```
deactivate
```

---

## Troubleshooting

**`python3.12: command not found`**
Your system does not have Python 3.12 on the PATH. Install it and try again,
or use the full path to the interpreter (e.g. `/usr/local/bin/python3.12`).

**`ModuleNotFoundError: No module named 'src'`**
Run commands from the repository root (the directory that contains the `src/`
folder), not from inside `src/`.

**`No module named venv`**
Some Linux distributions ship Python without the `venv` module. Install it
with:

```
sudo apt install python3.12-venv   # Debian / Ubuntu
```

**Wrong Python version in the virtual environment**
Delete `.venv/` and recreate it using `python3.12 -m venv .venv` explicitly.
Using `python3 -m venv .venv` may resolve to a different Python version.

**Virtual environment not activated**
If you see import errors or the wrong Python version, make sure you have
activated the virtual environment before running any commands. Check with:

```
which python   # Linux / macOS
where python   # Windows
```

The path should point inside `.venv/`.
