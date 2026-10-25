# Docker

Two images, pinned deliberately (see `REPRODUCING.md` for why version pins were previously missing). The core image has been built and run end-to-end; the export image is built in CI (see "Verified" below).

## Core pipeline (notebooks 01, 02, 02b, 02d, 03, 04)

**Prerequisite:** Docker Desktop installed and running (check the system tray: the engine has to actually be up, not just the app open).

```bash
docker build -t kardiosense-research .
```

Run this from the repository root (the directory containing this file and `Dockerfile`).

First build pulls the pinned `pytorch/pytorch:2.2.0-cuda12.1-cudnn8-runtime` base image (~3.6GB) and installs the pinned packages on top. Expect roughly 8-10 minutes on a normal connection, almost all of it the base image download.

Then run it detached, with a local folder mounted in for your data:

```bash
mkdir -p data
docker run -d --name kardiosense-research -p 8888:8888 -v "$(pwd)/data:/workspace/data" kardiosense-research
```

Get the access URL (includes a per-container token) from the logs:

```bash
docker logs kardiosense-research
```

Look for a line like:
```
http://127.0.0.1:8888/tree?token=<token>
```
Open that in a browser. You'll see `notebooks/` (all public notebooks, read-only) and `data/` (your `-v` mount; `KARDIOSENSE_BASE_DIR` inside the container already points here).

**Windows + Git Bash:** if you run the `docker run` command above from Git Bash (the default terminal that ships with Git for Windows), Git Bash's automatic path conversion can silently mangle the container-side half of the `-v` argument (`/workspace/data` gets rewritten as if it were a Windows path), producing a bind mount that looks like it worked but never actually shares files with the container. If your `data/` folder stays empty while the container is clearly writing files, prefix the command with `MSYS_NO_PATHCONV=1`:
```bash
MSYS_NO_PATHCONV=1 docker run -d --name kardiosense-research -p 8888:8888 -v "$(pwd)/data:/workspace/data" kardiosense-research
```
PowerShell, cmd.exe, macOS, and Linux shells are not affected by this.

**When you're done:**
```bash
docker stop kardiosense-research && docker rm kardiosense-research
```

## TFLite export (notebook 05 only)

Kept in a separate image (`Dockerfile.tflite_export`) because TensorFlow's CUDA/cuDNN requirements conflict with the core image's PyTorch pairing. It is a CPU image on `python:3.12-slim` with TensorFlow 2.21, PyTorch 2.14 (CPU build), onnx 1.23 and onnxruntime 1.31, all pinned in `requirements-export.txt`:

```bash
docker build -f Dockerfile.tflite_export -t kardiosense-tflite-export .
docker run -p 8888:8888 kardiosense-tflite-export
```

The two images take their pins from separate files: the core image from `requirements.txt`, the export image from `requirements-export.txt`. The export pins cover the export the notebook ships: the PyTorch model, its ONNX export with an onnxruntime check, and the native Keras and TFLite export in section 10. The onnx2tf cells before section 10 (the conversion path that section replaced) also need onnx2tf, sng4onnx and onnxsim, which are left out on purpose: onnx2tf 2.x requires onnx 1.20.1, which has open security advisories. Install them in a separate, throwaway environment if you want to rerun that part.

## What this does and doesn't fix

**Fixes:** the OS/CUDA/cuDNN/Python-package version drift that comes from relying on "whatever Colab has today." Every package version in both images is pinned and will stay pinned unless someone deliberately bumps them.

**Doesn't fix:** these notebooks were authored for Colab, so their setup cells call `google.colab.drive.mount()` / `google.colab.auth()`. Those calls are now wrapped in a `try`/`except ImportError` in every notebook, so outside Colab (e.g. inside this container) they're skipped automatically and `BASE_DIR` (via `KARDIOSENSE_BASE_DIR`) is used as-is, with no manual per-notebook editing needed for that part any more. What this does *not* fix: `02d_fusion_external_mimic.ipynb` still needs its own BigQuery authentication outside Colab (e.g. `gcloud auth application-default login`) and a PhysioNet-credentialed `KARDIOSENSE_GCP_PROJECT`, and every notebook still expects its input data (downloaded or pre-populated under `KARDIOSENSE_BASE_DIR`) and, for notebooks past 01/02, the checkpoints produced by earlier notebooks in the run order (see `REPRODUCING.md`).

## Verified

The core image (`kardiosense-research`) has been built and run, including inside the container itself: the pinned base image resolved, every pinned package installed with no version conflicts, the container started, and the Jupyter server responded (HTTP 200) on `http://127.0.0.1:8888`. With the `-v` bind mount working (see the Windows + Git Bash note above), a notebook's setup cell was executed inside the running container via `docker exec`: it correctly detected it was outside Colab, skipped the Drive mount without crashing, and built the `KARDIOSENSE_BASE_DIR` directory tree on the host through the volume mount, confirming the guard works in the actual pinned environment, not just on a bare host Python. What's still **not** verified: a full notebook run end-to-end inside the container (the actual data download, preprocessing, and training/evaluation cells beyond the setup cell) has not been recorded here; treat that as the next verification step.

The TFLite export image (`kardiosense-tflite-export`) is built by CI (`docker.yml`) whenever `Dockerfile.tflite_export` or `requirements-export.txt` changes, so its pins are known to install together. The notebook itself has not been run end to end inside it; check an export with your own weights and the real PTB-XL test fold, as the notebook does.
