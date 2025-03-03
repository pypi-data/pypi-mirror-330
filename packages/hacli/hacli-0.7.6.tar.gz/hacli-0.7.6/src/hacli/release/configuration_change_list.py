import json
import os
from datetime import datetime
from string import Template

import typer
from git import GitCommandError
from rich import print
from typing_extensions import Annotated

from hacli.release.create_release_note_md import add_configuration_pr_link
from hacli.utils.git_commands import LocalGitCommand

app = typer.Typer()


@app.command(name="configuration_change_list",
             help=" 生成版本间配置文件变化的 md 文件",
             short_help="生成版本间配置变化文档")
def configuration_change_list(
        pre_release: Annotated[str, typer.Argument(help="前一个版本号，例如：1.0.0")],
        cur_release: Annotated[str, typer.Argument(help="当前版本号，例如：1.1.0")]
):
    configuration_changes = []
    service_name_convert_mappings = json.loads(os.environ["TAG_SERVICE_NAME_CONVERT_MAPPINGS"])
    configuration_changes.append("## Configuration Change List\n")
    command = LocalGitCommand(True).repo
    for product in service_name_convert_mappings.values():
        commands = (
            Template(os.environ["RELEASE_NOTE_CONFIGURATION_GIT_COMMAND"])
            .safe_substitute(product=product,
                             pre_release=pre_release,
                             cur_release=cur_release)
        )
        formatted_product = product.replace("-", " ").title()
        print("Start to generate [red]configuration changes[/red] for product: [red]{}[/red]".format(formatted_product))
        try:
            configuration_changes.append(f"\n### {formatted_product}\n")
            print("    >>> Command for [red]{formatted_product}[/red]: ", commands)
            log_output = command.git.execute(command=commands, shell=True)
            configuration_changes.append(add_configuration_pr_link(log_output))
        except GitCommandError as e:
            configuration_changes.append(e.stderr)

    final_str = '\n'.join(configuration_changes)
    print("---------------------------- [green] End Generation [/green] ----------------------------")
    print("Final MD Content: \n", final_str)
    now = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
    file_name = f"Configuration Change List [{pre_release}-{cur_release}]-{now}"
    with open(f"{file_name}.md", "w", encoding="utf-8") as f:
        f.write(final_str)

    return final_str
