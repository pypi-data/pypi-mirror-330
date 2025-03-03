import typer
from rich import print
from typing_extensions import Annotated

from ..utils.git_commands import LocalGitCommand

app = typer.Typer()


@app.command(
    name="create_local_repo_branch",
    help="创建一个新的 Git 分支",
    short_help="创建新分支"
)
def create_local_repo_branch(
        branch: Annotated[str, typer.Argument(
            help="新分支的名称",
            show_default=False,
        )],
        base_branch: Annotated[str, typer.Option(
            help="基础分支名称",
            show_default=True,
        )] = "master",
        is_global: Annotated[bool, typer.Option(
            "--global",
            "-g",
            help="是否在全局 Git 仓库中创建分支",
            show_default=True
        )] = False,
):
    """
    创建一个新的 Git 分支。
    Args:
        branch: 新分支的名称
        base_branch: 基础分支名称，默认为 master
        is_global: 是否为全局分支
    """
    git_cmd = LocalGitCommand(is_global)
    git_cmd.branch.create_branch(branch, base_branch)
    print(
        f"Branch [bold green]{branch}[/bold green] created from [bold green]{base_branch}[/bold green] in dir [bold green]{git_cmd.working_dir}[/bold green]")


@app.command(
    name="create_local_release_branch",
    help="创建一个新的 Release 分支",
    short_help="创建本地Release分支"
)
def create_local_release_branch(
        release: Annotated[str, typer.Argument(
            help="release",
            show_default=False,
        )]
):
    """
    创建一个新的 Git 分支。
    Args:
        release: 新分支的名称
    """
    git_cmd = LocalGitCommand(False)
    release_branch = f"release/{release}-Application-Deployment"
    git_cmd.branch.create_branch(release_branch, "master")
    print(
        f"Branch [bold green]{release_branch}[/bold green] created from [bold green]master[/bold green] in dir [bold green]{git_cmd.working_dir}[/bold green]")


@app.command(
    name="create_global_rollout_update_branch",
    help="创建一个新的 Application Rollout Update 分支",
    short_help="创建Global Rollout Update分支"
)
def create_global_rollout_update_branch(
        release: Annotated[str, typer.Argument(
            help="release",
            show_default=False,
        )],
        task_id: Annotated[str, typer.Argument(
            help="task_id",
            show_default=False,
        )]
):
    """
    创建一个新的 Git 分支。
    Args:
        release: 新分支的名称
        task_id: work item id
    """
    # TODO remove work_item id 自动创建
    # Task 355970: Application Rollout Update in CN 25.1.3 的 name
    git_cmd = LocalGitCommand(True)
    release_branch = f"feature/{task_id}-Application-Rollout-Update-in-CN-{release}"
    git_cmd.branch.create_branch(release_branch, "master")
    print(
        f"Branch [bold green]{release_branch}[/bold green] created from [bold green]master[/bold green] in dir [bold green]{git_cmd.working_dir}[/bold green]")
