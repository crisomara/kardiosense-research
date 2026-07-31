# Docker

Two images, pinned deliberately (see `REPRODUCING.md` for why version pins were previously missing).

## Core pipeline (notebooks 01, 02, 02b, 02d, 03, 04, 06-11)

```
docker build -t kardiosense-research .
docker run -p 8888:8888 -v $(pwd)/data:/workspace/data kardiosense-research
```

Opens Jupyter on port 8888 with the notebooks mounted read-only under `/workspace/notebooks`. Point it at your own local copy of PTB-XL/CODE-15%/NHANES via the `-v` mount above; `KARDIOSENSE_BASE_DIR` inside the container already defaults to `/workspace/data`.

## TFLite export (notebook 05 only)

Kept in a separate image (`Dockerfile.tflite_export`) because TensorFlow/ONNX's CUDA/cuDNN requirements conflict with the core image's PyTorch pairing:

```
docker build -f Dockerfile.tflite_export -t kardiosense-tflite-export .
docker run -p 8888:8888 kardiosense-tflite-export
```

## What this does and doesn't fix

**Fixes:** the OS/CUDA/cuDNN/Python-package version drift that comes from relying on "whatever Colab has today." Every package version in both images is pinned and will stay pinned unless someone deliberately bumps them.

**Doesn't fix:** these notebooks were authored for Colab and their setup cells call `google.colab.drive.mount()` / `google.colab.auth()`, which don't exist outside Colab. Running a notebook headlessly inside either image (e.g. via `nbconvert`/`papermill`) requires either editing that one setup cell to skip the Colab-only mount/auth calls, or running the notebook interactively in the Jupyter UI these images expose and doing that edit by hand once. Nothing else about the notebooks' logic needed to change for this — only that first cell is Colab-specific.

**Not attempted:** no image was built or run as part of creating these Dockerfiles — there's no Docker execution available in the environment that wrote them. Treat the pinned versions as a reasonable, deliberate starting point, not a verified-working configuration, until you've built and run it once.
