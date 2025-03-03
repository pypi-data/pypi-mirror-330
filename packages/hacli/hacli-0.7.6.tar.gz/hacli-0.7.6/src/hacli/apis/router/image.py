from typing import Dict, Union, Any

from fastapi import APIRouter

router = APIRouter()

from hacli.image import (
    check_service_image_imported as check_image,
    purge_local_images as purge,
    import_global_service_images as service_images,
    import_global_external_images as external_images,
)


@router.get("/check", tags=["Image"], description="""
            ## 检查各个产品的服务是否已经导入, 请确保 `az login`已登录
""")
async def check_service_image_imported(
) -> Dict[str, Union[str, Dict[str, str]]]:
    return check_image.check_service_image_imported()


@router.get("/purge/local", tags=["Image"], description="""
           ## 请在 terminal 确认是否要执行 pipeline
""")
async def purge_local_images(
):
    return purge.purge_local_images()


@router.get("/import/global/service", tags=["Image"], description="""
            ## 导入 global 各个 product 对应 release tag 的镜像
            请在 terminal 确认是否要执行 pipeline
""")
async def import_global_service(
) -> dict[str, Any]:
    return service_images.import_global_service_images()


@router.get("/import/external", tags=["Image"], description="""
            ## 导入 global 基础的第三方镜像
            请在 terminal 确认是否要执行 pipeline
""")
async def import_global_external(
) -> Union[dict, None]:
    return external_images.import_global_external_images()
