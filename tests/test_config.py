"""
Test configuration commandline tools
"""
from tljh import config
from contextlib import redirect_stdout
import io
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



