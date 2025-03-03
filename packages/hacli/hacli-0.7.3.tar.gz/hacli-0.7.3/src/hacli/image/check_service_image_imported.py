import json
import os
from pathlib import Path
from string import Template

import typer
from azure.containerregistry import ContainerRegistryClient
from azure.core.exceptions import ResourceNotFoundError
from azure.identity import DefaultAzureCredential
from rich import print
from typing_extensions import Dict, Union

from ..tag.get_global_rollout_status import get_global_rollout_status

app = typer.Typer()


@app.command(
    name="check_service_image_imported",
    help="检查服务镜像是否已导入到容器注册表",
    short_help="检查服务镜像状态"
)
def check_service_image_imported() -> Dict[str, Union[str, Dict[str, str]]]:
    """
    检查所有服务的镜像是否已成功导入到 Azure 容器注册表。

    此命令会检查配置中定义的所有服务的镜像是否已经成功导入到容器注册表中。
    检查基于全局发布状态中的标签进行验证。

    环境变量:
        PROJECT_LOCAL_GIT_LOCAL_WORKING_DIR: 项目本地 Git 工作目录
        SERVICES_CONFIGURATION_DIR: 服务配置目录
        SERVICES_DEPLOYMENT_SETTING_DIR_TEMPLATE: 服务部署设置目录模板
        SERVICES_DEPLOYMENT_SETTING_SERVICE_KEY_TEMPLATE: 服务部署设置键模板
        PROJECT_LOCAL_ACR_URL: Azure 容器注册表 URL

    输出:
        - 对于每个服务，如果所有镜像都已导入，显示绿色成功消息
        - 如果有镜像未找到或检查出错，显示红色错误消息

    Examples:
        检查所有服务镜像：
            $ hacli image check_service_image_imported

    注意:
        - 需要 Azure 认证凭据
        - 确保所有必需的环境变量已正确设置
        - 检查基于服务配置文件中定义的服务列表
    """
    rollout_tags: dict[str, str] = get_global_rollout_status()

    ENDPOINT = os.environ["PROJECT_LOCAL_ACR_URL"]

    credential = DefaultAzureCredential()
    result = {}
    with ContainerRegistryClient(ENDPOINT, credential) as client:
        for product, tag in rollout_tags.items():
            services = get_service_names(product)
            print(f"Start to check services for product [red]{product}[/red] with tag [red]{tag}[/red]", services)
            service_checked_result = {}
            for service in services:
                print(f"  Start to check service [red]{service}[/red]")
                try:
                    client.get_tag_properties(repository=f"service/{service}", tag=tag)
                except ResourceNotFoundError:
                    service_checked_result[service] = f"Not Found For Tag {tag}"
                except Exception as e:
                    service_checked_result[service] = f"Not Found {tag}"

            if service_checked_result:
                result[product] = service_checked_result
            else:
                result[product] = f"All images imported"
            print("-------------------------------------------------------------------------- \n")
    print("Checked result", result)
    return result


def get_service_names(product: str):
    """
    获取指定目录下包含 'cn' 子目录的所有服务名称。

    Args:
        :param product: product-management, service-management, user-management, vehicle-management, system
    Returns:
        包含 'cn' 子目录的服务名称列表
    """
    project_dir = os.environ["PROJECT_LOCAL_GIT_LOCAL_WORKING_DIR"]
    product_configuration_root_dir = os.environ["SERVICES_CONFIGURATION_DIR"]

    product_configuration_dir = Path(project_dir) / product_configuration_root_dir / product
    directories_with_valid_services = []
    for subdir, dirs, files in os.walk(product_configuration_dir):
        if 'cn' in dirs:
            directories_with_valid_services.append(os.path.basename(subdir))

    service_deployment_setting_template = os.environ["SERVICES_DEPLOYMENT_SETTING_DIR_TEMPLATE"]
    deployment_setting_service_key_template = os.environ["SERVICES_DEPLOYMENT_SETTING_SERVICE_KEY_TEMPLATE"]
    substitute = Template(service_deployment_setting_template).safe_substitute(product=product)
    service_configuration_setting_file = Path(project_dir) / str(substitute)

    with open(service_configuration_setting_file, "r") as f:
        loads: dict = json.loads(f.read())
        product_key_in_file = Template(deployment_setting_service_key_template).safe_substitute(product=product)
        product_services: dict = loads.get(product_key_in_file)
        if services_from_configuration := product_services.get("services"):
            directories_with_valid_services = [
                item for item in directories_with_valid_services
                if item in services_from_configuration
            ]

    return directories_with_valid_services
