import os
import re
from datetime import datetime, date
from string import Template
from typing import List

import typer
from azure.devops.v7_0.work_item_tracking import WorkItemReference
from git import GitCommandError
from rich import print
from tabulate import tabulate
from typing_extensions import Annotated

from hacli.tag.get_global_rollout_status import get_global_rollout_status
from hacli.utils.ado import AzureDevOpsClient
from hacli.utils.git_commands import LocalGitCommand

app = typer.Typer()


@app.command(name="create_release_note_md",
             help="生成版本发布说明文档，自动收集指定服务在两个版本之间的所有提交记录",
             short_help="生成版本发布说明文档")
def create_release_note_md(
        pre_release: Annotated[str, typer.Argument(help="前一个版本号，例如：1.0.0")],
        cur_release: Annotated[str, typer.Argument(help="当前版本号，例如：1.1.0")]
):
    """
        生成版本发布说明文档（Release Notes）。

        此命令会自动收集指定服务在两个版本之间的所有 Git 提交记录，并生成一个格式化的 Markdown 文档。
        文档按服务进行分类，每个服务的提交记录都会单独列出。

        Args:
            pre_release: 前一个版本的标签名称（例如：1.0.0）
            cur_release: 当前版本的标签名称（例如：1.1.0）

        环境变量:
            GIT_COMMANDS_RELEASE_NOTE: Git 命令模板，用于获取提交记录
                模板变量：
                - ${service}: 服务名称
                - ${pre_release}: 前一个版本号
                - ${cur_release}: 当前版本号

        示例:
            $ hacli git create_release_note_md 1.0.0 1.1.0

        注意:
            - 需要确保环境变量 GIT_COMMANDS_RELEASE_NOTE 已正确设置
            - 该命令会在全局 Git 仓库中执行
            - 如果某个服务获取提交记录失败，会显示错误信息但不会中断整个过程
    """
    print("---------------------------- [green] Basic information Part [/green] ----------------------------")
    # 1. generate basic information [tag]
    product_tag_dict: dict[str, str] = get_global_rollout_status()
    basic_information: list[str] = generate_basic_information(cur_release, product_tag_dict)

    print("---------------------------- [green] Release Note Part [/green] ----------------------------")
    # 2. generate release note for product
    basic_information.append("\n## 2. What’s new? \n")
    client = AzureDevOpsClient(os.environ["RELEASE_NOTE_WORK_ITEM_PROJECT"])
    wiql, product_query_condition_dict = generate_wiql(cur_release, list(product_tag_dict.keys()))
    items_reference: List[WorkItemReference] = client.work_items.query_work_item_reference(wiql)
    if not items_reference: raise Exception("Release note not found")
    print(f"Work Item Reference: ",
          [{
              "url": item.url,
              "web_edit_url": item.url.replace("_apis/wit/workItems", "_workitems/edit")
          } for item in items_reference])
    work_item_ids = [work_item.id for work_item in items_reference]
    items = client.work_items.query_working_items(work_item_ids,
                                                  fields=["System.Title", "System.Description",
                                                          "Custom.ReleaseNotesv2"])
    if not items: raise Exception("Release note not found")

    work_items_dict = {work_item.fields.get('System.Title'): work_item.fields.get('Custom.ReleaseNotesv2',
                                                                                  'No Release Notes Available') for
                       work_item in
                       items}

    for product, work_item_condition in product_query_condition_dict.items():
        work_item_title = re.search(r"'(.*?)'", work_item_condition).group(1)
        basic_information.append(f"### {product} \n")
        print(f"Start to generate [red]release notes[/red] for product: [red]{product}[/red]")
        if product_release_note_content := work_items_dict.get(work_item_title):
            print(f"    >>>  Add [red]release notes[/red] for product: [red]{product}[/red]")
            basic_information.append(handle_release_note_from_work_item(str(product_release_note_content)) + "\n")
        else:
            print(f"    >>>  Not Found[red]release notes[/red] for product: [red]{product}[/red]")
            basic_information.append(f"No Release Notes Available For {product} As field missing \n")

    print("---------------------------- [green] Configuration Part [/green] ----------------------------")
    # 3. generate configuration changes
    basic_information.append("## 3. Configuration \n")
    command = LocalGitCommand(True).repo
    for product in product_tag_dict.keys():
        commands = (
            Template(os.environ["RELEASE_NOTE_CONFIGURATION_GIT_COMMAND"])
            .safe_substitute(product=product,
                             pre_release=pre_release,
                             cur_release=cur_release)
        )
        formatted_product = product.replace("-", " ").title()
        print("Start to generate [red]configuration changes[/red] for product: [red]{}[/red]".format(formatted_product))
        try:
            basic_information.append(f"\n### {formatted_product}\n")
            print("    >>> Command for [red]{formatted_product}[/red]: ", commands)
            log_output = command.git.execute(command=commands, shell=True)
            basic_information.append(add_configuration_pr_link(log_output))
        except GitCommandError as e:
            basic_information.append(e.stderr)

    final_str = "\n".join(basic_information)
    print("---------------------------- [green] End Generation [/green] ----------------------------")
    print("Final MD Content: \n", final_str)

    with open(f"{basic_information[0].replace("#", "")}.md", "w", encoding="utf-8") as f:
        f.write(str(final_str))

    return final_str


def generate_basic_information(release: str, product_tag_dict: dict[str, str]) -> list[str]:
    current_date = date.today()
    year, week, _ = current_date.isocalendar()
    md_header = os.environ["RELEASE_NOTE_MD_TITLE_TEMPLATE"].format(cw=str(week + 1).zfill(2), year=str(year))
    basic_information = [md_header, f"**Sprint: {release}** \n"]

    # Date table
    headers = ["Date", "Maintenance History", "By"]
    rows = [
        [datetime.now().strftime("%Y-%m-%d"), "Created and completed this note",
         os.environ.get("AUTH", "<Replace Your Name>")]
    ]

    date_table = tabulate(rows, headers=headers, tablefmt="pipe", colalign=("center", "center", "center"))
    basic_information.append(date_table)

    # Tag Table
    basic_information.append("\n## 1. Versions/Tags to be deployed on Approval \n")
    table_rows_data = [(key.replace("-", " ").title(), value) for key, value in product_tag_dict.items()]
    headers = ["Product Cluster", "Version/Tag"]
    product_cluster = tabulate(table_rows_data, headers=headers, tablefmt="pipe", colalign=("center", "center"))
    basic_information.append(product_cluster)
    return basic_information


def handle_release_note_from_work_item(content: str) -> str:
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(content, 'html.parser')

    markdown_output = []
    for link in soup.find_all('a'):
        url = link['href']
        text = link.text.strip()
        try:
            task_id, description = text.split(': ', 1)
            markdown_output.append(f"- [{task_id}]({url}): {description}")
        except Exception as e:
            markdown_output.append(f"- [{text}]({url})")
    return '\n'.join(markdown_output)


def add_configuration_pr_link(configuration_item_list: str) -> str:
    pr_link_url = os.environ["RELEASE_NOTE_CONFIGURATION_LIST_PR_LINK_URL"]

    res = [
        re.sub(r'Merged PR (\d+)', lambda m: f'Merged [PR {m.group(1)}]({pr_link_url}{m.group(1)})', s)
        for s in configuration_item_list.split("\n")
    ]
    return "\n".join(res)


def generate_wiql(release: str, products: list) -> (str, dict[str, str]):
    wiql_query_template = os.environ["RELEASE_NOTE_WIQL_QUERY_TEMPLATE"]
    wiql_product_item_template = os.environ["RELEASE_NOTE_WIQL_PRODUCT_ITEM_TEMPLATE"]
    product_query_condition_dict = {
        product.replace("-", " ").title(): wiql_product_item_template.format(release=release,
                                                                             product=product.replace("-", " ").title())
        for product in products}

    conditions = " OR ".join(
        list(product_query_condition_dict.values())
    )

    wiql_query = wiql_query_template.format(conditions=conditions)
    return wiql_query, product_query_condition_dict
