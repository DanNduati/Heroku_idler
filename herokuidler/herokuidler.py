from pathlib import Path
from typing import Any, Dict, List, NamedTuple

from herokuidler import DB_READ_ERROR, ID_ERROR
from herokuidler.database import StorageHandler


class CurrentUrl(NamedTuple):
    url: List[Dict[str, Any]]
    error: int


class UrlController:
    def __init__(self, db_path: Path) -> None:
        self._storage_handler = StorageHandler(db_path)

    def add(self, url: str) -> CurrentUrl:
        """Add a new url to the json storage"""
        url = {"url": url}
        read = self._storage_handler.read_urls()
        if read.error == DB_READ_ERROR:
            return CurrentUrl(url, read.error)
        read.url_list.append(url)
        write = self._storage_handler.write_urls(read.url_list)
        return CurrentUrl(url, write.error)

    def get_url_list(self) -> List[Dict[str, Any]]:
        read = self._storage_handler.read_urls()
        return read.url_list

    def remove(self, url_id: int) -> CurrentUrl:
        """Remove a url from the json storage by its index"""
        read = self._storage_handler.read_urls()
        if read.error:
            return CurrentUrl({}, read.error)
        try:
            url = read.url_list.pop(url_id - 1)
        except IndexError:
            return CurrentUrl({}, ID_ERROR)
        write = self._storage_handler.write_urls(read.url_list)
        return CurrentUrl(url, write.error)
