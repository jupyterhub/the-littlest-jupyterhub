"""Setup tljh logging"""
import logging
import os

from .config import INSTALL_PREFIX


def init_logging():
    """Setup default tljh logger"""
    logger = logging.getLogger("tljh")
    os.makedirs(INSTALL_PREFIX, exist_ok=True)

    # check if any log handlers are already registered
    # don't reconfigure logs if handlers are already configured
    # e.g. happens in pytest, which hooks up log handlers for reporting
    # or if this function is called twice
    if logger.hasHandlers():
        return
    file_logger = logging.FileHandler(os.path.join(INSTALL_PREFIX, "installer.log"))
    file_logger.setFormatter(logging.Formatter("%(asctime)s %(message)s"))
    logger.addHandler(file_logger)

    stderr_logger = logging.StreamHandler()
    stderr_logger.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(stderr_logger)
    logger.setLevel(logging.INFO)
