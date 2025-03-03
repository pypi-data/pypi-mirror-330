from fastapi import APIRouter

from hacli.tag import get_global_rollout_status as rollout_status

router = APIRouter()


@router.get("/rollout/tags",
            tags=["Tag"],
            description="""
             ## 获取 global 当前 appr 各个服务的 release tag
""")
async def get_tags(
) -> dict[str, str]:
    return rollout_status.get_global_rollout_status()
