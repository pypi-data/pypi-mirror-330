import typer

from . import create_release_note_md

app = typer.Typer()

app.add_typer(create_release_note_md.app)
