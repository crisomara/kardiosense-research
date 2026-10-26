# Contributing

Thank you for helping to check and improve this research code. By contributing you agree that your contribution is published under this repository's licence (`LICENSE`, PolyForm Noncommercial 1.0.0).

## What belongs here

- Code, notebooks and documentation that let other researchers inspect, rerun and test the methods.
- Aggregate results only: metrics, plots and summary tables.

What never belongs here:

- Trained model weights or exported models (`.pt`, `.onnx`, `.tflite` and similar).
- Datasets, records, or any row about an individual patient or participant, including in notebook outputs.
- Keys, passwords, tokens, email addresses (other than the public contact in `README.md`) or paths from your own machine.

The commit hooks and CI stop the most common cases, but you are responsible for what you commit. Clear a notebook's outputs before committing it if they show individual records.

## Set up once per clone

```bash
pip install -r requirements-ci.txt
pip install pre-commit==4.7.0
pre-commit install
```

## The code standard

| What | Rules | Where they live |
|---|---|---|
| Python and the code cells of notebooks | Ruff: errors, likely bugs, import order, modern syntax for Python 3.10, security checks, and a fixed layout (100 columns, double quotes) | `ruff.toml` |
| Every text file | UTF-8, LF line endings, a final newline, no trailing spaces | `.editorconfig` |
| Notebooks | Valid nbformat, at most 5 MB each | `scripts/check_notebooks.py` |
| Secrets | No keys or passwords in commits | `.gitleaks.toml` |

The code targets Python 3.10 because the core Docker image runs it. A rule is switched off for a file only in `ruff.toml`, with the reason next to it. A `# noqa` comment names the rule and says why.

## How it is checked

1. **On your machine.** The hooks run on the files in each commit and fix what they can. If a hook changes a file, the commit stops: look at the change, add the file again and commit again.
2. **In a pull request.** `ci.yml` runs Ruff over the whole repository, validates the notebooks, checks that no weights or data files are tracked and runs the tests. `security.yml` runs gitleaks, pip-audit, CodeQL, dependency review and actionlint.

Run the same checks locally:

```bash
ruff check . && ruff format --check .
python scripts/check_notebooks.py
python -m pytest -q
```

## Pull requests

- Branch from `main` and open a pull request into `main`.
- Say what changed and why. If a change can alter a reported result, say which notebook and which number.
- Commit messages: a short summary line, then what changed and why.
