#!/usr/bin/bash
set -exuo pipefail

# Set up defaults for configurable env vars
TLJH_INSTALL_PREFIX=${TLJH_INSTALL_PREFIX:-/opt/tljh}
TLJH_INSTALL_PIP_SPEC=${TLJH_INSTALL_PIP_SPEC:-git+https://github.com/yuvipanda/the-littlest-jupyterhub.git}
TLJH_INSTALL_PIP_FLAGS=${TLJH_INSTALL_PIP_FLAGS:---no-cache-dir}


function install_miniconda {
    CONDA_DIR=${1}
    CONDA_VERSION=4.5.4
    if [ -e ${CONDA_DIR}/bin/conda ]; then
        if [ "$(${CONDA_DIR}/bin/conda -V)" == "conda ${CONDA_VERSION}" ]; then
            # The given ${CONDA_DIR} already has a conda with given version
            return
        fi
    fi

    URL="https://repo.continuum.io/miniconda/Miniconda3-${CONDA_VERSION}-Linux-x86_64.sh"
    INSTALLER_PATH=/tmp/miniconda-installer.sh

    curl -o ${INSTALLER_PATH} ${URL}
    chmod +x ${INSTALLER_PATH}

    # Only MD5 checksums are available for miniconda
    # Can be obtained from https://repo.continuum.io/miniconda/
    MD5SUM="a946ea1d0c4a642ddf0c3a26a18bb16d"

    if ! echo "${MD5SUM}  ${INSTALLER_PATH}" | md5sum  --quiet -c -; then
        echo "md5sum mismatch for ${INSTALLER_PATH}, exiting!"
        exit 1
    fi

    bash ${INSTALLER_PATH} -u -b -p ${CONDA_DIR}

    # Allow easy direct installs from conda forge
    ${CONDA_DIR}/bin/conda config --system --add channels conda-forge

    # Do not attempt to auto update conda or dependencies
    ${CONDA_DIR}/bin/conda config --system --set auto_update_conda false
    ${CONDA_DIR}/bin/conda config --system --set show_channel_urls true
}

HUB_CONDA_DIR=${TLJH_INSTALL_PREFIX}/hub
install_miniconda ${HUB_CONDA_DIR}
${HUB_CONDA_DIR}/bin/pip install --upgrade ${TLJH_INSTALL_PIP_FLAGS} ${TLJH_INSTALL_PIP_SPEC}

${HUB_CONDA_DIR}/bin/python3 -m tljh.installer
