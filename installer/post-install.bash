#!/usr/bin/bash
set -euo pipefail

# Run by the installer after the hub environment has been set up.

export PATH=${PREFIX}/bin:$PATH

pip install --no-cache-dir -e /home/yuvipanda/code/littlest-jupyterhub

python3 -m tljh.installer
