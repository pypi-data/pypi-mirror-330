from fastapi import APIRouter
from fastapi.params import Query
from starlette.responses import PlainTextResponse

from hacli.release.create_release_note_md import create_release_note_md
from hacli.release.configuration_change_list import configuration_change_list
from hacli.release.release_checkout_date import release_checkout_date

router = APIRouter()


@router.get("/notes", tags=["Release"], response_class=PlainTextResponse)
async def get_release_notes(
        pre_release: str = Query(
            ...,
            title="Previous Release",
            description="前一个版本的标签名称",
            example="25.1.1",
            min_length=1
        ),
        cur_release: str = Query(
            ...,
            title="Current Release",
            description="当前版本的标签名称",
            example="25.1.2",
            min_length=1
        )
) -> str:
    """
        生成版本发布说明文档（Release Notes）的 md 文件
    """
    return create_release_note_md(pre_release=pre_release, cur_release=cur_release)


@router.get("/configuration/changes", tags=["Release"], response_class=PlainTextResponse)
async def get_configuration_change_list(
        pre_release: str = Query(
            ...,
            title="Previous Release",
            description="前一个版本的标签名称",
            example="25.1.1",
            min_length=1
        ),
        cur_release: str = Query(
            ...,
            title="Current Release",
            description="当前版本的标签名称",
            example="25.1.2",
            min_length=1
        )
) -> str:
    """
        生成版本间配置文件变化的 md 文件
    """
    return configuration_change_list(pre_release=pre_release, cur_release=cur_release)


@router.get("/checkout/date", tags=["Release"], response_class=PlainTextResponse)
async def get_release_checkout_date(
        release: str = Query(
            ...,
            title="Release",
            description="版本名称",
            example="25.1.1",
            min_length=1
        )
) -> str:
    """
        release 从 master checkout 的 时间， 和分支的相关信息
    """
    return release_checkout_date(release=release)


# TODO ADD configuration changes rollback infor