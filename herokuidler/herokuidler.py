from pathlib import Path
from typing import Any, Dict, NamedTuple
from herokuidler.database import StorageHandler

class CurrentUrl(NamedTuple):
    todo: Dict[str, Any]
    error: int
    
class UrlController:
    def __init__(self,db_path:Path)-> None:
        self._storage_handler = StorageHandler(db_path)
