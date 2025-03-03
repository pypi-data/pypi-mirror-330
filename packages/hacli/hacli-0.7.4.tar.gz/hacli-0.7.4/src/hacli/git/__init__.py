import typer

from . import git_ops

app = typer.Typer()

app.add_typer(git_ops.app)
