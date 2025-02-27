import sys

import typer

from . import deploy
from . import git
from . import image
from . import tag
from .utils.envs import load_yaml_env_vars


def start():
    app = typer.Typer(
        pretty_exceptions_show_locals=False,
        no_args_is_help=True,
        help="hacli for operations",
        add_completion=False,
        callback=load_yaml_env_vars
    )

    app.add_typer(deploy.app, name="deploy", help="部署服务")
    app.add_typer(tag.app, name="tag", help="获取 tag 相关")
    app.add_typer(git.app, name="git", help="本地 git 操作仓库")
    app.add_typer(image.app, name="image", help="镜像相关")

    try:
        app()
    except Exception as e:
        typer.secho(e, err=True, bold=True, fg=typer.colors.RED)
        sys.exit(1)
