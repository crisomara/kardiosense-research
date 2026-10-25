# CLAUDE.md

Instructions for Claude Code sessions in this repository. They match `CONTRIBUTING.md`; read it for the full standard.

## What this repository is

Public, research-only code (PolyForm Noncommercial 1.0.0) so that outside researchers can inspect and rerun the KardioSense methods. Keep it clean and short: no dead code, no commented-out experiments.

## Never commit

- Model weights or exported models, datasets, or records.
- Any per-record patient or participant row, including in notebook outputs.
- Keys, passwords, tokens, email addresses (other than the public contact in `README.md`) or local paths.

## Writing code

- Follow `ruff.toml` and `.editorconfig`. Before committing, run `pre-commit run --files <the files you changed>` and keep its fixes.
- Python 3.10 (the core Docker image), 100 columns, double quotes, sorted imports.
- Ruff rewrites notebook code cells only. Do not clear or rewrite stored outputs unless they show individual records.
- Each change to `scripts/` comes with a test; run `python -m pytest`.

## Git

- Open pull requests into `main`. Never merge, force-push or rewrite history without the owner's explicit go-ahead.
- Keep the Co-Authored-By line at the end of commit messages.

## Writing documents

Documents for outside readers use plain prose: short sentences, no em dashes, no filler. Every number can be traced to the notebook or run it came from.
