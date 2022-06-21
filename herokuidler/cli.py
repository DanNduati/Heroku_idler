from pathlib import Path
from typing import List, Optional

import typer

from herokuidler import (  # isort:skip
    ERRORS,
    __app_name__,
    __version__,
    config,
    database,
    herokuidler,
)

app = typer.Typer()


@app.command()
def init(
    db_path: str = typer.Option(
        str(database.DEFAULT_DB_FILE_PATH),
        "--db-path",
        "-db",
        prompt="use this as the url json storage location?",
    )
) -> None:
    """Initialize the url json storage"""
    config_init_error = config.init_app(db_path)
    if config_init_error:
        typer.secho(
            f'Creating config file failed with "{ERRORS[config_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    db_init_error = database.init_database(Path(db_path))
    if db_init_error:
        typer.secho(
            f'Creating database failed with "{ERRORS[db_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(f"The urls json storage is {db_path}", fg=typer.colors.GREEN)


def get_url() -> herokuidler.UrlController:
    if config.CONFIG_FILE_PATH.exists():
        db_path = database.get_database_path(config.CONFIG_FILE_PATH)
    else:
        typer.secho(
            'Configuration file not found. Please, run "herokuidler init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    if db_path.exists():
        return herokuidler.UrlController(db_path)
    else:
        typer.secho(
            'Json storage file not found. Please, run "herokuidler init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return
