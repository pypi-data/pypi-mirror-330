import sys

import typer
import uvicorn
from fastapi import FastAPI
from rich import print
from typing_extensions import Annotated

from . import deploy
from . import git
from . import image
from . import release
from . import tag
from .utils.envs import load_yaml_env_vars

# Refers to <a href="https://github.com/zxiaosi/vue3-fastapi.git"></a>
fast_api = FastAPI(
    title="Hacli API",
    description="Hacli REST API Service",
    version="1.0.0"
)
from .apis.register.router import register_router
from .apis.register.exception import register_exception

# TODO
# git.exc.GitCommandError: Cmd('git') failed due to: exit code(1)
#   cmdline: git checkout master1
#   stderr: 'error: pathspec 'master1' did not match any file(s) known to git'

register_exception(fast_api)
register_router(fast_api)


def start():
    app = typer.Typer(
        pretty_exceptions_show_locals=False,
        no_args_is_help=True,
        help="hacli for operations",
        add_completion=False,
        callback=load_yaml_env_vars
    )

    @app.command(help="开启 web 服务")
    def serve(
            port: Annotated[int, typer.Option("--port", "-p", help="服务端口号")] = 8000,
            host: Annotated[str, typer.Option("--host", "-h", help="服务监听地址", )] = "0.0.0.0"
    ):
        print(f"host [green]{host}[/green] started port [green]{port}[/green]")
        uvicorn.run(
            "hacli.main:fast_api",
            host=host,
            port=port,
            reload=True,
            log_level="critical",
        )

    app.add_typer(deploy.app, name="deploy", help="部署服务")
    app.add_typer(tag.app, name="tag", help="获取 tag 相关")
    app.add_typer(git.app, name="git", help="本地 git 操作仓库")
    app.add_typer(image.app, name="image", help="镜像相关")
    app.add_typer(release.app, name="release", help="release相关")

    try:
        app()

    except Exception as e:
        typer.secho(e, err=True, bold=True, fg=typer.colors.RED)
        sys.exit(1)
