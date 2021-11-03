import pytest
from tljh import utils
import subprocess
import logging


def test_run_subprocess_exception(mocker):
    logger = logging.getLogger("tljh")
    mocker.patch.object(logger, "error")
    with pytest.raises(subprocess.CalledProcessError):
        utils.run_subprocess(["/bin/bash", "-c", "echo error; exit 1"])
    logger.error.assert_called_with("error\n")


def test_run_subprocess(mocker):
    logger = logging.getLogger("tljh")
    mocker.patch.object(logger, "debug")
    utils.run_subprocess(["/bin/bash", "-c", "echo success"])
    logger.debug.assert_called_with("success\n")
