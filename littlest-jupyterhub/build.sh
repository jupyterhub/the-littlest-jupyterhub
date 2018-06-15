#!/bin/bash
set -euo pipefail

# FIXME: Should this coming from conda-forge instead?
$PYTHON -m pip install --no-deps --ignore-installed \
        jupyterhub-systemdspawner==0.9.10 \
        jupyterhub-dummyauthenticator==0.3.1