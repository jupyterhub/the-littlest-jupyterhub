#!/usr/bin/bash
set -euo pipefail

# Run by the installer after the hub environment has been set up.

export PATH=${PREFIX}/bin:$PATH

pip install --no-cache-dir git+https://github.com/yuvipanda/the-littlest-jupyterhub.git

python3 -m tljh.installer
