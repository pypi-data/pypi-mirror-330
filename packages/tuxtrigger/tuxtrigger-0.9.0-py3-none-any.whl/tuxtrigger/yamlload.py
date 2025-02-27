from pathlib import Path

import yaml


def _yaml_load(data):
    return yaml.load(data, Loader=yaml.FullLoader)


def yaml_file_read(yaml_path: Path) -> dict:
    with yaml_path.open("r") as file:
        loaded_yaml = _yaml_load(file)
    return loaded_yaml
