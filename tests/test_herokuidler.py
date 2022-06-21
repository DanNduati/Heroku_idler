import json

import pytest
from typer.testing import CliRunner

from herokuidler import (  # isort:skip
    DB_READ_ERROR,
    SUCCESS,
    __app_name__,
    __version__,
    cli,
    herokuidler,
)

runner = CliRunner()


def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}" in result.stdout


@pytest.fixture
def mock_json_file(tmp_path):
    url = [{"url": "https://gentle-dusk-50795.herokuapp.com/ping"}]
    db_file = tmp_path / "url.json"
    with db_file.open("w") as db:
        json.dump(url, db, indent=4)
    return db_file


test_data1 = {
    "url": "https://gentle-dusk-50795.herokuapp.com/ping",
}
test_data2 = {
    "url": "https://fastapi-dan.herokuapp.com/",
}


def test_add(mock_json_file):
    url_adder = herokuidler.UrlController(mock_json_file)
    assert url_adder.add(test_data1) == expected
    read = url_adder._storage_handler.read_urls()
    assert len(read) == 2
