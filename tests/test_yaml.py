from tljh.yaml import yaml


def test_no_empty_flow(tmpdir):
    path = tmpdir.join("config.yaml")
    with path.open("w") as f:
        f.write("{}")
    # load empty config file
    with path.open("r") as f:
        config = yaml.load(f)
    # set a value
    config["key"] = "value"
    # write to a file
    with path.open("w") as f:
        yaml.dump(config, f)
    # verify that it didn't use compact '{}' flow-style
    with path.open("r") as f:
        content = f.read()
    assert content.strip() == "key: value"
