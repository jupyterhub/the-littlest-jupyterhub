"""
Unit test  functions in installer.py
"""
from tljh import installer
import os


def test_ensure_node():
    installer.ensure_node()
    assert os.path.exists('/usr/bin/node')
