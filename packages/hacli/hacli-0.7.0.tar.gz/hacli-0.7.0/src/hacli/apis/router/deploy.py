from typing import Dict, Union

from fastapi import APIRouter
from fastapi.params import Query

from hacli.apis.schemas.deploy_models import DeployRequest

router = APIRouter(tags=["Deploy"])

from hacli.deploy.check_services_deployment_status import check_services_deployment_status

from hacli.deploy.build_up_inactive_cluster import build_up_inactive_cluster
from hacli.deploy.sync_global_repo import sync_global_repo
from hacli.deploy.deploy_inactive_services import deploy_inactive_services
from hacli.deploy.deploy_inactive_shared_services import deploy_inactive_shared_services
from hacli.deploy.toggle_active_cluster import toggle_active_cluster
from hacli.deploy.update_active_service_config import update_active_service_config
from hacli.deploy.teardown_inactive_cluster import teardown_inactive_cluster


@router.get("/sync_global_repo", description="""
            ## trigger sync global repository pipeline \n
            if return None, it means you cancel to trigger sync global repository
""")
def sync_global_repo_api() -> Union[dict, None]:
    return sync_global_repo()


@router.get("/build_up_inactive_cluster", description="""
            ## trigger build up inactive cluster pipeline \n
            if return None, it means you cancel to build up inactive cluster
""")
def build_up_inactive_cluster_api(
        release: str = Query(
            ...,
            title="Release",
            description="release的名称",
            example="25.1.1",
            min_length=1
        ),
) -> Union[dict, None]:
    return build_up_inactive_cluster(release=release)


@router.get("/deploy_inactive_services", description="""
            ## trigger deploy inactive services pipeline \n
            if return None inner the dict, it means you cancel to build up the product services \n
            - release: 发布的版本号 [required]
            - product_names: 要部署的产品名称列表，可指定多个 [optional]
            - deploy_all_product: 是否部署所有产品 [default: false]
            
""")
def deploy_inactive_services_api(deploy_request: DeployRequest
                                 ) -> dict:
    return deploy_inactive_services(release=deploy_request.release, product_names=deploy_request.product_names,
                                    deploy_all_product=deploy_request.deploy_all_product)


@router.get("/deploy_inactive_shared_services", description="""
            ## trigger build up inactive cluster pipeline \n
            if return None, it means you cancel to deploy inactive shared services
""")
def deploy_inactive_shared_services_api(
        release: str = Query(
            ...,
            title="Release",
            description="release的名称",
            example="25.1.1",
            min_length=1
        ),
        tag: str = Query(
            ...,
            title="Tag",
            description="tag",
            example="25.1.1-dc9247d4cfb6f11a19bc499ec4baa6048b5ba7b0",
            min_length=1
        ),
) -> Union[dict, None]:
    return deploy_inactive_shared_services(release=release, tag=tag)


@router.get("/toggle_active_cluster", description="""
            ## trigger toggle active cluster pipeline \n
            if return None, it means you cancel to toggle active cluster
""")
def toggle_active_cluster_api(
        release: str = Query(
            ...,
            title="Release",
            description="release的名称",
            example="25.1.1",
            min_length=1
        )
) -> Union[dict, None]:
    return toggle_active_cluster(release=release)


@router.get("/update_active_service_config", description="""
            ## trigger update active service config pipeline \n
            if return None, it means you cancel to update active service config

            Args:
                - release: 要更新的版本号，例如 "1.0.0"
                - product: 产品名称(pm, sm, um, vm, shared)，将自动转换为大写
                - service: 服务名称，支持的值: 请查看各个产品对应的服务
""")
def update_active_service_config_api(
        release: str = Query(
            ...,
            title="Release",
            description="release的名称",
            example="25.1.1",
            min_length=1
        ),
        product: str = Query(
            ...,
            title="Product",
            description="product的名称",
            example="<Check Your Product>",
            min_length=1
        ),
        service: str = Query(
            ...,
            title="Service",
            description="product下的 service",
            example="<Check Your Service>",
            min_length=1
        )
) -> Union[dict, None]:
    return update_active_service_config(release=release, product=product, service=service)


@router.get("/teardown_inactive_cluster", description="""
            ## trigger teardown inactive cluster pipeline \n
            if return None, it means you cancel to teardown inactive cluster
""")
def teardown_inactive_cluster_api(
        release: str = Query(
            ...,
            title="Release",
            description="release的名称",
            example="25.1.1",
            min_length=1
        ),
) -> Union[dict, None]:
    return teardown_inactive_cluster(release=release)


@router.get("/check/deployment/status", description="""
            ## 检查当前部署是否已经完成, 请确保 `az login`已登录
""")
async def check_services_deployment_status_api(
) -> Dict[str, str]:
    return check_services_deployment_status()
