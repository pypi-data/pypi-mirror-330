import json
import os

import typer
from rich import print
from tabulate import tabulate
from typing_extensions import Annotated

from hacli.utils.git_commands import LocalGitCommand

app = typer.Typer()


@app.command(name="release_checkout_date",
             help="release 从 master checkout 的 时间， 和分支的相关信息",
             short_help="release 创建的日期，分支信息")
def release_checkout_date(
        release: Annotated[str, typer.Argument(help="版本号，例如25.1.1")],
):
    git_cmd = LocalGitCommand(True)

    service_name_convert_mappings = json.loads(os.environ["TAG_SERVICE_NAME_CONVERT_MAPPINGS"])

    table_data = []
    headers = ["Service", "Version", "Checkout Date", "Message", "Hot Fix"]

    for product in service_name_convert_mappings.values():
        branch_name = os.environ["RELEASE_BRANCH_NAME_TEMPLATE"].format(product=product, release=release)

        if not git_cmd.branch.branch_exists(branch_name):
            table_data.append([product, f"Branch {branch_name} Not Found", "-", "-", "-"])
            continue

        merge_base = git_cmd.branch.get_merge_base(branch_name, "master")
        if not merge_base:
            table_data.append([product, "Merge base not found", "-", "-", "-"])
            continue

        commit_date, commit_message = git_cmd.commit.get_latest_commit_info(merge_base)
        if not commit_date or not commit_message:
            table_data.append([product, "No commits found", "-", "-", "-"])
            continue

        # 判断是否有 Hot Fix
        new_commits = git_cmd.commit.has_hotfixes(merge_base, branch_name)

        hotfix_info = f"Yes ({len(new_commits)})" if new_commits else "No"

        # 添加到表格数据
        table_data.append([product, branch_name, f"`{commit_date}`", commit_message.strip(), hotfix_info])

    # 生成 Markdown 格式表格
    markdown_table = tabulate(table_data, headers=headers, tablefmt="github")

    # 保存到 Markdown 文件
    with open("Product Release Checkout Date.md", "a+", encoding="utf-8") as f:
        f.write(f"\n# Product Release {release} Checkout Date\n")
        f.write(markdown_table + "\n")

    # 打印 Markdown 表格
    res = '\n'.join([f"# Product Release {release} Checkout Report\n", markdown_table])
    print(res)
    return res
