# Pinned environment for the core PyTorch-based pipeline: notebooks 01, 02,
# 02b, 02d, 03, 04, 06-11. Does NOT cover 05_export_tflite.ipynb, which needs
# TensorFlow/ONNX and would conflict with this image's CUDA/cuDNN pairing --
# see Dockerfile.tflite_export for that one instead.
#
# Base image is pinned to an exact tag deliberately: this repo's original
# Colab runs had no captured version pins (see REPRODUCING.md), so this is a
# new, explicit baseline going forward, not a reconstruction of what any
# individual notebook originally ran under. If this exact tag is ever pulled
# from Docker Hub, substitute any recent pytorch/pytorch:<ver>-cudaXX.X-cudnnN-runtime
# tag -- the pinning discipline matters more than this specific version.
FROM pytorch/pytorch:2.2.0-cuda12.1-cudnn8-runtime

WORKDIR /workspace

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Pinned as of this Dockerfile's creation -- bump deliberately, not silently.
RUN pip install --no-cache-dir \
    jupyter==1.0.0 \
    nbconvert==7.16.4 \
    papermill==2.6.0 \
    wfdb==4.1.2 \
    h5py==3.11.0 \
    neurokit2==0.2.9 \
    imbalanced-learn==0.12.3 \
    xgboost==2.0.3 \
    shap==0.45.1 \
    optuna==3.6.1 \
    pyreadstat==1.2.7 \
    seaborn==0.13.2 \
    google-cloud-bigquery==3.25.0

COPY notebooks/ /workspace/notebooks/

# These notebooks were authored for Colab and call google.colab.drive.mount()
# / google.colab.auth() in their setup cells, which do not exist outside
# Colab. Running them here requires either:
#   (a) interactively editing that one setup cell to point at a local/mounted
#       data directory (BASE_DIR is already overridable via the
#       KARDIOSENSE_BASE_DIR env var -- see REPRODUCING.md), or
#   (b) stripping the Colab-specific mount/auth cell before headless
#       execution with nbconvert/papermill.
# This image pins the environment; it does not rewrite the notebooks.
ENV KARDIOSENSE_BASE_DIR=/workspace/data

EXPOSE 8888
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
