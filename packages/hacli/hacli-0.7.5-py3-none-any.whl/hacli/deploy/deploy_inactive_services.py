from typing import Optional, List

import typer
from rich import print
from typing_extensions import Annotated

from ..tag.get_global_rollout_status import get_global_rollout_status
from ..utils.ado import execute_pipeline

app = typer.Typer()

product_tag_mappings = {
    "pm": "pm",
    "sm": "sm",
    "um": "um",
    "vm": "vm",
    "sys": "st"
}


@app.command(
    name="deploy_inactive_services",
    help="部署服务到非活动集群",
    short_help="部署到非活动集群"
)
def deploy_inactive_services(
        release: Annotated[str, typer.Argument(
            help="发布版本号",
            show_default=False
        )],
        product_names: Annotated[Optional[List[str]], typer.Option(
            "--product",
            "-p",
            help="要部署的产品名称列表，可指定多个",
            show_default=False
        )] = None,
        deploy_all_product: Annotated[bool, typer.Option(
            "--all-product",
            "-a",
            help="是否部署所有产品",
            show_default=True
        )] = False
) -> dict:
    """
    将指定服务部署到非活动集群。

    此命令用于将指定的服务部署到非活动集群中。可以选择部署特定的产品或所有产品。
    部署时会自动获取全局发布状态，并使用相应的标签进行部署。

    Args:
        release: 要部署的版本号，例如 "1.0.0"
        product_names: 要部署的产品列表，可选值：pm, sm, um, vm, sys
        deploy_all_product: 是否部署所有产品，当设置为 True 时会忽略 product_names 参数

    环境变量:
        DEPLOY_PIPELINES_DEPLOY_INACTIVE_SERVICES_NAME: 部署流水线名称
        DEPLOY_PIPELINES_DEPLOY_INACTIVE_SERVICES_PARAMETERS: 部署流水线参数配置

    Examples:
        部署特定产品：
            $ hacli deploy deploy_inactive_services 1.0.0 --product pm --product sm

        部署所有产品：
            $ hacli deploy deploy_inactive_services 1.0.0 --all-product

    注意:
        - 必须指定 --product 或 --all-product 其中之一
        - 确保指定的产品名称在支持列表中（pm/sm/um/vm/sys）
        - 执行前请确保已正确设置所需的环境变量
    """
    tags_to_deploy: dict[str, str] = get_global_rollout_status()

    if not deploy_all_product and not product_names:
        typer.secho("Either specify product name or specify deploy all products.", fg=typer.colors.RED)
        return {"error": "Either specify product name or specify deploy all products."}

    deploy_product = product_names if not deploy_all_product else list(product_tag_mappings.keys())
    valid_deploy_product = {product for product in deploy_product if product in product_tag_mappings}

    res = {}
    for product in valid_deploy_product:
        product_name = product.upper()
        tag = tags_to_deploy[product_tag_mappings[product.lower()].upper()]
        result = execute_pipeline(release=release,
                                  pipeline_name_env_key="DEPLOY_PIPELINES_DEPLOY_INACTIVE_SERVICES_NAME",
                                  pipeline_parameter_env_key="DEPLOY_PIPELINES_DEPLOY_INACTIVE_SERVICES_PARAMETERS",
                                  product=product_name, tag=tag)
        res[product] = result

    print("Deploying inactive services: ", res)
    return res
