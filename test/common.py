from pathlib import Path


def resource_path(name):
    return Path(__file__).parent / "resources" / name