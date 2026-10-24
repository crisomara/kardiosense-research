import sys
from pathlib import Path

import nbformat
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import check_notebooks

REPO_ROOT = Path(__file__).resolve().parent.parent


def _write_nb(path: Path, outputs=None) -> Path:
    nb = nbformat.v4.new_notebook()
    cell = nbformat.v4.new_code_cell("print('hi')")
    cell.outputs = outputs or []
    nb.cells = [nbformat.v4.new_markdown_cell("# t"), cell]
    nbformat.write(nb, path)
    return path


def test_valid_notebook_passes(tmp_path):
    p = _write_nb(tmp_path / "ok.ipynb", [nbformat.v4.new_output("stream", text="hi\n")])
    r = check_notebooks.inspect_notebook(p, max_mb=5)
    assert r.problem is None
    assert (r.code_cells, r.markdown_cells, r.outputs) == (1, 1, 1)


def test_error_and_image_outputs_are_counted(tmp_path):
    outputs = [
        nbformat.v4.new_output("error", ename="E", evalue="boom", traceback=[]),
        nbformat.v4.new_output("display_data", data={"image/png": "iVBORw0KGgo="}),
    ]
    r = check_notebooks.inspect_notebook(_write_nb(tmp_path / "e.ipynb", outputs), max_mb=5)
    assert r.error_outputs == 1
    assert r.image_outputs == 1
    assert r.problem is None


def test_oversized_notebook_fails(tmp_path):
    p = _write_nb(tmp_path / "big.ipynb")
    r = check_notebooks.inspect_notebook(p, max_mb=0.000001)
    assert r.problem and "budget" in r.problem


def test_schema_violation_fails(tmp_path):
    p = tmp_path / "bad.ipynb"
    p.write_text(
        '{"nbformat": 4, "nbformat_minor": 5, "metadata": {}, "cells": [{"cell_type": "code"}]}'
    )
    r = check_notebooks.inspect_notebook(p, max_mb=5)
    assert r.problem and r.problem.startswith("invalid notebook")


def test_not_json_fails(tmp_path):
    p = tmp_path / "broken.ipynb"
    p.write_text("not json")
    assert check_notebooks.inspect_notebook(p, max_mb=5).problem


def test_main_exit_codes(tmp_path, capsys):
    good = _write_nb(tmp_path / "good.ipynb")
    assert check_notebooks.main([str(good)]) == 0
    assert check_notebooks.main([str(good), "--max-mb", "0.000001"]) == 1
    assert "| Notebook |" in capsys.readouterr().out


@pytest.mark.parametrize(
    "nb_path", sorted((REPO_ROOT / "notebooks").glob("*.ipynb")), ids=lambda p: p.name
)
def test_committed_notebooks_are_valid(nb_path):
    r = check_notebooks.inspect_notebook(nb_path, max_mb=check_notebooks.DEFAULT_MAX_MB)
    assert r.problem is None, r.problem
