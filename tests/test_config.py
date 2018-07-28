"""
Test configuration commandline tools
"""
from tljh import config
from contextlib import redirect_stdout
import io
import pytest
import tempfile


def test_set_no_mutate():
    conf = {}

    new_conf = config.set_item_in_config(conf, 'a.b', 'c')
    assert new_conf['a']['b'] == 'c'
    assert conf == {}

def test_set_one_level():
    conf = {}

    new_conf = config.set_item_in_config(conf, 'a', 'b')
    assert new_conf['a'] == 'b'

def test_set_multi_level():
    conf = {}

    new_conf = config.set_item_in_config(conf, 'a.b', 'c')
    new_conf = config.set_item_in_config(new_conf, 'a.d', 'e')
    new_conf = config.set_item_in_config(new_conf, 'f', 'g')
    assert new_conf == {
        'a': {'b': 'c', 'd': 'e'},
        'f': 'g'
    }

def test_set_overwrite():
    """
    We can overwrite already existing config items.

    This might be surprising destructive behavior to some :D
    """
    conf = {
        'a': 'b'
    }

    new_conf = config.set_item_in_config(conf, 'a', 'c')
    assert new_conf == {'a': 'c'}

    new_conf = config.set_item_in_config(new_conf, 'a.b', 'd')
    assert new_conf == {'a': {'b': 'd'}}

    new_conf = config.set_item_in_config(new_conf, 'a', 'hi')
    assert new_conf == {'a': 'hi'}


def test_add_to_config_one_level():
    conf = {}

    new_conf = config.add_item_to_config(conf, 'a.b', 'c')
    assert new_conf == {
        'a': {'b': ['c']}
    }


def test_add_to_config_zero_level():
    conf = {}

    new_conf = config.add_item_to_config(conf, 'a', 'b')
    assert new_conf == {
        'a': ['b']
    }

def test_add_to_config_multiple():
    conf = {}

    new_conf = config.add_item_to_config(conf, 'a.b.c', 'd')
    assert new_conf == {
        'a': {'b': {'c': ['d']}}
    }

    new_conf = config.add_item_to_config(new_conf, 'a.b.c', 'e')
    assert new_conf == {
        'a': {'b': {'c': ['d', 'e']}}
    }


def test_remove_from_config():
    conf = {}

    new_conf = config.add_item_to_config(conf, 'a.b.c', 'd')
    new_conf = config.add_item_to_config(new_conf, 'a.b.c', 'e')
    assert new_conf == {
        'a': {'b': {'c': ['d', 'e']}}
    }

    new_conf = config.remove_item_from_config(new_conf, 'a.b.c', 'e')
    assert new_conf == {
        'a': {'b': {'c': ['d']}}
    }

def test_remove_from_config_error():
    with pytest.raises(ValueError):
        config.remove_item_from_config({}, 'a.b.c', 'e')

    with pytest.raises(ValueError):
        config.remove_item_from_config({'a': 'b'}, 'a.b', 'e')

    with pytest.raises(ValueError):
        config.remove_item_from_config({'a': ['b']}, 'a', 'e')


def test_show_config():
    """
    Test stdout output when showing config
    """
    conf = """
# Just some test YAML
a:
  b:
  - h
  - 1
    """.strip()


    with tempfile.NamedTemporaryFile() as tmp:
        tmp.write(conf.encode())
        tmp.flush()

        out = io.StringIO()
        with redirect_stdout(out):
            config.show_config(tmp.name)

    assert out.getvalue().strip() == conf



