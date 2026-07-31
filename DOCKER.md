# Docker

Two images, pinned deliberately (see `REPRODUCING.md` for why version pins were previously missing). The core image has been built and run end-to-end (see "Verified" below); the TFLite export image has not.

## Core pipeline (notebooks 01, 02, 02b, 02d, 03, 04, 06-11)

**Prerequisite:** Docker Desktop installed and running (check the system tray — the engine has to actually be up, not just the app open).

```bash
cd public
docker build -t kardiosense-research .
```

First build pulls the pinned `pytorch/pytorch:2.2.0-cuda12.1-cudnn8-runtime` base image (~3.6GB) and installs the pinned packages on top — expect roughly 8-10 minutes on a normal connection, almost all of it the base image download.

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
Open that in a browser. You'll see `notebooks/` (all 13 public notebooks, read-only) and `data/` (your `-v` mount — `KARDIOSENSE_BASE_DIR` inside the container already points here).

**When you're done:**
```bash
docker stop kardiosense-research && docker rm kardiosense-research
```

## TFLite export (notebook 05 only)

Kept in a separate image (`Dockerfile.tflite_export`) because TensorFlow/ONNX's CUDA/cuDNN requirements conflict with the core image's PyTorch pairing:

```bash
docker build -f Dockerfile.tflite_export -t kardiosense-tflite-export .
docker run -p 8888:8888 kardiosense-tflite-export
```

This one has **not** been built or run — treat it the same way the core image was treated before it was verified (see below).

## What this does and doesn't fix

**Fixes:** the OS/CUDA/cuDNN/Python-package version drift that comes from relying on "whatever Colab has today." Every package version in both images is pinned and will stay pinned unless someone deliberately bumps them.

**Doesn't fix:** these notebooks were authored for Colab and their setup cells call `google.colab.drive.mount()` / `google.colab.auth()`, which don't exist outside Colab. Running a notebook inside the container still requires editing that one setup cell to skip the Colab-only mount/auth calls and just use `BASE_DIR` directly — nothing else about the notebooks' logic needs to change for this.

## Verified

The core image (`kardiosense-research`) has actually been built and run: the pinned base image resolved, every pinned package installed with no version conflicts, the container started, and the Jupyter server responded (HTTP 200) on `http://127.0.0.1:8888`. What was *not* verified: actually executing any notebook inside the container (the Colab-mount-cell edit above still needs doing first, by hand, per notebook).

The TFLite export image is unverified — nobody has built it yet.
