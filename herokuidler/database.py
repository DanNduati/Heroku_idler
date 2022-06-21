import configparser
import json
from pathlib import Path
from typing import Any, Dict, List, NamedTuple

from herokuidler import DB_READ_ERROR, DB_WRITE_ERROR, JSON_ERROR, SUCCESS

DEFAULT_DB_FILE_PATH = Path.home().joinpath("." + Path.home().stem + "_urls.json")


def get_database_path(config_file: Path) -> Path:
    """Return the current path to the urls database"""
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    return Path(config_parser["General"]["database"])


def init_database(db_path: Path) -> int:
    """Create the urls database"""
    try:
        db_path.write_text("[]")  # empty url list
        return SUCCESS
    except OSError:
        return DB_WRITE_ERROR


class StorageResponse(NamedTuple):
    url_list: List[str]
    error: int


class StorageHandler:
    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path

    def read_urls(self) -> StorageResponse:
        try:
            with self._db_path.open("r") as db:
                try:
                    return StorageResponse(json.load(db), SUCCESS)
                except json.JSONDecodeError:
                    return StorageResponse([], JSON_ERROR)
        except OSError:
            return ([], DB_READ_ERROR)

    def write_urls(self, url_list: List[Dict[str, Any]]) -> StorageResponse:
        try:
            with self._db_path.open("w") as db:
                json.dump(url_list, db, indent=4)
            return StorageResponse(url_list, SUCCESS)
        except OSError:
            return StorageResponse([], DB_WRITE_ERROR)
