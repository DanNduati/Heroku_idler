import configparser
from pathlib import Path

import typer

from herokuidler import (  # isort:skip
    DB_WRITE_ERROR,
    DIR_ERROR,
    FILE_ERROR,
    SUCCESS,
    __app_name__,
)

CONFIG_DIR_PATH = Path(typer.get_app_dir(__app_name__))
CONFIG_FILE_PATH = CONFIG_DIR_PATH.joinpath("config.ini")


def _init_config_file() -> int:
    try:
        CONFIG_DIR_PATH.mkdir(exist_ok=True)
    except OSError:
        return DIR_ERROR
    try:
        CONFIG_FILE_PATH.touch(exist_ok=True)
    except OSError:
        return FILE_ERROR
    return SUCCESS


def _create_config(db_path: str) -> int:
    config_parser = configparser.ConfigParser()
    config_parser["General"] = {"database": db_path}
    try:
        with CONFIG_FILE_PATH.open("w") as file:
            config_parser.write(file)
    except OSError:
        return FILE_ERROR
    return SUCCESS


def init_app(db_path: str) -> int:
    """Initialize the application"""
    # Create the config file
    config_code = _init_config_file()
    if config_code != SUCCESS:
        return config_code
    # Add configurations to the config file
    config_code = _create_config(db_path)
    if config_code != SUCCESS:
        return config_code
    return SUCCESS
