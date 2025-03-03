# from fastapi import FastAPI, Request
# from fastapi import Query
# from fastapi.responses import JSONResponse
# from fastapi.responses import PlainTextResponse
# from typing_extensions import Dict, Union, Any
#
# from hacli.apis.schemas.git import CreateBranchRequest
# from hacli.release.create_release_note_md import create_release_note_md
#
# app = FastAPI(
#     title="Hacli API",
#     description="Hacli REST API Service",
#     version="1.0.0"
# )
#
#
#
#
# # from hacli.deploy import check_services_deployment_status as deployment_status
# #
# #
# # @app.get("/check/deployment/status", tags=["Deploy"], description="""
# #             ## 检查当前部署是否已经完成, 请确保 `az login`已登录
# # """)
# # async def check_services_deployment_status(
# # ) -> Dict[str, str]:
# #     return deployment_status.check_services_deployment_status()
#
#
#
#
# from hacli.git import create_local_repo_branch as git_ops
#
#
# @app.post(
#     "/check/deployment/status", )
# def create_repo_branch(request: CreateBranchRequest):
#     return git_ops.create_local_repo_branch(request.branch, request.base_branch, request.is_global)
#
#
# # TODO use cache if possible
# @app.get("/release/notes", tags=["Release"], response_class=PlainTextResponse)
# async def get_release_notes(
#         pre_release: str = Query(
#             ...,
#             title="Previous Release",
#             description="前一个版本的标签名称",
#             example="1.0.0",
#             min_length=1
#         ),
#         cur_release: str = Query(
#             ...,
#             title="Current Release",
#             description="当前版本的标签名称",
#             example="1.1.0",
#             min_length=1
#         )
# ) -> str:
#     """
#         生成版本发布说明文档（Release Notes）的 md 文件
#     """
#     return create_release_note_md(pre_release=pre_release, cur_release=cur_release)
#
#
#
#
# # from hacli.image import (
# #     check_service_image_imported as check_image,
# #     purge_local_images as purge,
# #     import_global_service_images as service_images,
# #     import_global_external_images as external_images,
# # )
# #
# # @app.get("/check", tags=["Image"], description="""
# #             ## 检查各个产品的服务是否已经导入, 请确保 `az login`已登录
# # """)
# # async def check_service_image_imported(
# # ) -> Dict[str, Union[str, Dict[str, str]]]:
# #     return check_image.check_service_image_imported()
# #
# #
# # @app.get("/purge/local", tags=["Image"], description="""
# #             ## Purge 本地 acr 镜像, 请确保 `az login`已登录
# #             请在 terminal 确认是否要执行 pipeline
# # """)
# # async def purge_local_images(
# # ):
# #     return purge.purge_local_images()
# #
# #
# # @app.get("/import/global/service", tags=["Image"], description="""
# #             ## 导入 global 各个 product 对应 release tag 的镜像
# #             请在 terminal 确认是否要执行 pipeline
# # """)
# # async def import_global_service(
# # ) -> dict[str, Any]:
# #     return service_images.import_global_service_images()
# #
# #
# # @app.get("/import/external", tags=["Image"], description="""
# #             ## 导入 global 基础的第三方镜像
# #             请在 terminal 确认是否要执行 pipeline
# # """)
# # async def import_global_external(
# # ) -> Union[dict, None]:
# #     return external_images.import_global_external_images()
#
#
# # from hacli.tag.get_global_rollout_status import get_global_rollout_status
# #
# #
# # @app.get("/rollout/tags",
# #          tags=["Tag"],
# #          description="""
# #              ## 获取 global 当前 appr 各个服务的 release tag
# # """)
# # async def get_tags(
# # ) -> dict[str, str]:
# #     return get_global_rollout_status()
