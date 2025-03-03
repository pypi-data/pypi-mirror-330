import json
import os
import re

import typer
from azure.devops.v7_0.dashboard import Widget
from bs4 import BeautifulSoup
from markdown_it import MarkdownIt
from rich import print

from ..utils.ado import AzureDevOpsClient

app = typer.Typer()


# TODO use cache if possible
@app.command(
    name="get_global_rollout_status",
    help="获取全局发布状态信息",
    short_help="获取发布状态"
)
def get_global_rollout_status() -> dict[str, str]:
    """
    获取并显示全局发布状态信息。

    此命令从 Azure DevOps 仪表板获取当前活动集群中所有服务的发布标签信息。

    环境变量:
        PROJECT_GLOBAL_NAME: 全局项目名称
        TAG_TEAM: 团队名称
        TAG_DASHBOARD_ID: 仪表板 ID
        TAG_ACTIVE_CLUSTER_WIDGET_ID: 活动集群小部件 ID
        TAG_SERVICES_TAG_WIDGET_ID: 服务标签小部件 ID

    输出:
        以字典格式显示所有服务的标签信息：
        {
            "SERVICE1": "1.0.0",
            "SERVICE2": "v1.1.0",
            ...
        }

    Examples:
        获取发布状态：
            $ hacli tag get_global_rollout_status

    注意:
        - 需要正确配置 Azure DevOps 访问凭据
        - 确保所有环境变量已正确设置
    """
    client = AzureDevOpsClient(os.environ["PROJECT_GLOBAL_NAME"])

    tag_team = os.environ["TAG_TEAM"]
    tag_dashboard_id = os.environ["TAG_DASHBOARD_ID"]
    tag_active_cluster_widget_id = os.environ["TAG_ACTIVE_CLUSTER_WIDGET_ID"]
    tag_services_tag_widget_id = os.environ["TAG_SERVICES_TAG_WIDGET_ID"]

    widget: Widget = client.dashboard.get_widget_from_dashboard(team=tag_team,
                                                                dashboard_id=tag_dashboard_id,
                                                                widget_id=tag_active_cluster_widget_id)
    print("Start to get active cluster")
    green_clusters = [
        re.sub(r"[`]", "", match[0].strip())
        for match in re.findall(r"\| (.*?) \| (.*?) \| (.*?) \|", widget.settings)
        if "green" in match[1].lower() and "green" in match[2].lower()
    ]

    if not green_clusters: raise Exception("Active cluster was not found from global rollout status")
    active_cluster = green_clusters[0]
    print(f"Get to get active cluster [green]{active_cluster}[/green]")
    tag_widget: Widget = client.dashboard.get_widget_from_dashboard(team=tag_team,
                                                                    dashboard_id=tag_dashboard_id,
                                                                    widget_id=tag_services_tag_widget_id)
    md = MarkdownIt('js-default')
    html_content = md.render(tag_widget.settings)
    soup = BeautifulSoup(html_content, 'html.parser')

    result_map = {}
    for table in soup.find_all('table'):
        cluster_name = table.find('code').text.strip()
        cluster_data = {row.find_all('td')[0].text.strip(): row.find_all('td')[1].text.strip()
                        for row in table.find_all('tr')[1:]}

        result_map[cluster_name] = cluster_data

    if not result_map: raise Exception(f"Tags for active cluster {active_cluster} services were not found")
    print("Get tags for services")
    print(result_map)

    service_name_convert_mappings = json.loads(os.environ["TAG_SERVICE_NAME_CONVERT_MAPPINGS"])

    return {
        product: result_map.get(active_cluster).get(tag_key)
        for tag_key, product in service_name_convert_mappings.items() if tag_key in result_map.get(active_cluster)
    }
