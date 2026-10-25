"""Static checks for the committed notebooks (nothing is executed).

For every ``*.ipynb`` given (or every notebook under ``notebooks/`` by default):

* validate it against the nbformat JSON schema;
* fail if the file is larger than the size budget (outputs are kept on purpose
  in this repo as the record of each run, but a single notebook should not grow
  past the budget without someone noticing);
* report size, cell counts, output counts and any stored error outputs, as a
  table on stdout and, in GitHub Actions, in the job summary.

Usage: python scripts/check_notebooks.py [--max-mb 5] [paths...]
"""

from __future__ import annotations

import argparse
import os
import sys
from dataclasses import dataclass
from pathlib import Path

import nbformat

DEFAULT_MAX_MB = 5.0


@dataclass
class NotebookReport:
    path: Path
    size_bytes: int
    code_cells: int = 0
    markdown_cells: int = 0
    outputs: int = 0
    error_outputs: int = 0
    image_outputs: int = 0
    problem: str | None = None

    @property
    def size_mb(self) -> float:
        return self.size_bytes / 1_000_000


def inspect_notebook(path: Path, max_mb: float) -> NotebookReport:
    report = NotebookReport(path=path, size_bytes=path.stat().st_size)
    try:
        nb = nbformat.read(path, as_version=nbformat.NO_CONVERT)
        nbformat.validate(nb)
    except Exception as exc:  # any read/validation failure is a hard failure
        report.problem = f"invalid notebook: {type(exc).__name__}: {exc}".splitlines()[0]
        return report

    for cell in nb.cells:
        if cell.cell_type == "code":
            report.code_cells += 1
            for out in cell.get("outputs", []):
                report.outputs += 1
                if out.get("output_type") == "error":
                    report.error_outputs += 1
                if any(k.startswith("image/") for k in out.get("data", {})):
                    report.image_outputs += 1
        elif cell.cell_type == "markdown":
            report.markdown_cells += 1

    if report.size_mb > max_mb:
        report.problem = f"{report.size_mb:.2f} MB exceeds the {max_mb:g} MB budget"
    return report


def render_table(reports: list[NotebookReport]) -> str:
    lines = [
        "| Notebook | Size (MB) | Code cells | Outputs | Images | Stored errors | Status |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for r in reports:
        status = f"FAIL: {r.problem}" if r.problem else "ok"
        lines.append(
            f"| `{r.path.as_posix()}` | {r.size_mb:.2f} | {r.code_cells} | {r.outputs} "
            f"| {r.image_outputs} | {r.error_outputs} | {status} |"
        )
    total = sum(r.size_bytes for r in reports) / 1_000_000
    lines.append(f"\nTotal: {len(reports)} notebooks, {total:.2f} MB.")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("paths", nargs="*", type=Path)
    parser.add_argument("--max-mb", type=float, default=DEFAULT_MAX_MB)
    args = parser.parse_args(argv)

    paths = args.paths or sorted(Path("notebooks").glob("*.ipynb"))
    if not paths:
        print("No notebooks found.", file=sys.stderr)
        return 1

    reports = [inspect_notebook(p, args.max_mb) for p in paths]
    table = render_table(reports)
    print(table)

    summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_file:
        with open(summary_file, "a", encoding="utf-8") as fh:
            fh.write("## Notebook check\n\n" + table + "\n")

    failed = [r for r in reports if r.problem]
    for r in failed:
        print(f"::error file={r.path.as_posix()}::{r.problem}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
