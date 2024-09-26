"""
Test configuration commandline tools
"""

import os
import tempfile
from unittest import mock

import pytest

from tljh import config, configurer


def test_set_no_mutate():
    conf = {}

    new_conf = config.set_item_in_config(conf, "a.b", "c")
    assert new_conf["a"]["b"] == "c"
    assert conf == {}


def test_set_one_level():
    conf = {}

    new_conf = config.set_item_in_config(conf, "a", "b")
    assert new_conf["a"] == "b"


def test_set_multi_level():
    conf = {}

    new_conf = config.set_item_in_config(conf, "a.b", "c")
    new_conf = config.set_item_in_config(new_conf, "a.d", "e")
    new_conf = config.set_item_in_config(new_conf, "f", "g")
    assert new_conf == {"a": {"b": "c", "d": "e"}, "f": "g"}


def test_set_overwrite():
    """
    We can overwrite already existing config items.

    This might be surprising destructive behavior to some :D
    """
    conf = {"a": "b"}

    new_conf = config.set_item_in_config(conf, "a", "c")
    assert new_conf == {"a": "c"}

    new_conf = config.set_item_in_config(new_conf, "a.b", "d")
    assert new_conf == {"a": {"b": "d"}}

    new_conf = config.set_item_in_config(new_conf, "a", "hi")
    assert new_conf == {"a": "hi"}


def test_unset_no_mutate():
    conf = {"a": "b"}

    config.unset_item_from_config(conf, "a")
    assert conf == {"a": "b"}


def test_unset_one_level():
    conf = {"a": "b"}

    new_conf = config.unset_item_from_config(conf, "a")
    assert new_conf == {}


def test_unset_multi_level():
    conf = {"a": {"b": "c", "d": "e"}, "f": "g"}

    new_conf = config.unset_item_from_config(conf, "a.b")
    assert new_conf == {"a": {"d": "e"}, "f": "g"}
    new_conf = config.unset_item_from_config(new_conf, "a.d")
    assert new_conf == {"f": "g"}
    new_conf = config.unset_item_from_config(new_conf, "f")
    assert new_conf == {}


def test_unset_and_clean_empty_configs():
    conf = {"a": {"b": {"c": {"d": {"e": "f"}}}}}

    new_conf = config.unset_item_from_config(conf, "a.b.c.d.e")
    assert new_conf == {}


def test_unset_config_error():
    with pytest.raises(ValueError):
        config.unset_item_from_config({}, "a")

    with pytest.raises(ValueError):
        config.unset_item_from_config({"a": "b"}, "b")

    with pytest.raises(ValueError):
        config.unset_item_from_config({"a": {"b": "c"}}, "a.z")


def test_add_to_config_one_level():
    conf = {}

    new_conf = config.add_item_to_config(conf, "a.b", "c")
    assert new_conf == {"a": {"b": ["c"]}}


def test_add_to_config_zero_level():
    conf = {}

    new_conf = config.add_item_to_config(conf, "a", "b")
    assert new_conf == {"a": ["b"]}


def test_add_to_config_multiple():
    conf = {}

    new_conf = config.add_item_to_config(conf, "a.b.c", "d")
    assert new_conf == {"a": {"b": {"c": ["d"]}}}

    new_conf = config.add_item_to_config(new_conf, "a.b.c", "e")
    assert new_conf == {"a": {"b": {"c": ["d", "e"]}}}


def test_remove_from_config():
    conf = {}

    new_conf = config.add_item_to_config(conf, "a.b.c", "d")
    new_conf = config.add_item_to_config(new_conf, "a.b.c", "e")
    assert new_conf == {"a": {"b": {"c": ["d", "e"]}}}

    new_conf = config.remove_item_from_config(new_conf, "a.b.c", "e")
    assert new_conf == {"a": {"b": {"c": ["d"]}}}


def test_remove_from_config_error():
    with pytest.raises(ValueError):
        config.remove_item_from_config({}, "a.b.c", "e")

    with pytest.raises(ValueError):
        config.remove_item_from_config({"a": "b"}, "a.b", "e")

    with pytest.raises(ValueError):
        config.remove_item_from_config({"a": ["b"]}, "a", "e")


def test_reload_hub():
    with (
        mock.patch("tljh.systemd.restart_service") as restart_service,
        mock.patch("tljh.systemd.check_service_active") as check_active,
        mock.patch("tljh.config.check_hub_ready") as check_ready,
    ):
        config.reload_component("hub")
    restart_service.assert_called_with("jupyterhub")
    check_active.assert_called_with("jupyterhub")


def test_reload_proxy(tljh_dir):
    with (
        mock.patch("tljh.systemd.restart_service") as restart_service,
        mock.patch("tljh.systemd.check_service_active") as check_active,
    ):
        config.reload_component("proxy")
    restart_service.assert_called_with("traefik")
    check_active.assert_called_with("traefik")
    assert os.path.exists(os.path.join(config.STATE_DIR, "traefik.toml"))


def test_cli_no_command(capsys):
    config.main([])
    captured = capsys.readouterr()
    assert "usage:" in captured.out
    assert "positional arguments:" in captured.out


@pytest.mark.parametrize("arg, value", [("true", True), ("FALSE", False)])
def test_cli_set_bool(tljh_dir, arg, value):
    config.main(["set", "https.enabled", arg])
    cfg = configurer.load_config()
    assert cfg["https"]["enabled"] == value


def test_cli_set_int(tljh_dir):
    config.main(["set", "https.port", "123"])
    cfg = configurer.load_config()
    assert cfg["https"]["port"] == 123


def test_cli_unset(tljh_dir):
    config.main(["set", "foo.bar", "1"])
    config.main(["set", "foo.bar2", "2"])
    cfg = configurer.load_config()
    assert cfg["foo"] == {"bar": 1, "bar2": 2}

    config.main(["unset", "foo.bar"])
    cfg = configurer.load_config()

    assert cfg["foo"] == {"bar2": 2}


def test_cli_add_float(tljh_dir):
    config.main(["add-item", "foo.bar", "1.25"])
    cfg = configurer.load_config()
    assert cfg["foo"]["bar"] == [1.25]


def test_cli_remove_int(tljh_dir):
    config.main(["add-item", "foo.bar", "1"])
    config.main(["add-item", "foo.bar", "2"])
    cfg = configurer.load_config()
    assert cfg["foo"]["bar"] == [1, 2]
    config.main(["remove-item", "foo.bar", "1"])
    cfg = configurer.load_config()
    assert cfg["foo"]["bar"] == [2]


@pytest.mark.parametrize(
    "value, expected",
    [
        ("1", 1),
        ("1.25", 1.25),
        ("x", "x"),
        ("1x", "1x"),
        ("1.2x", "1.2x"),
        (None, None),
        ("", ""),
    ],
)
def test_parse_value(value, expected):
    assert config.parse_value(value) == expected


def test_show_config(capsys):
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
        config.show_config(tmp.name)
    out = capsys.readouterr().out
    assert out.strip() == conf
