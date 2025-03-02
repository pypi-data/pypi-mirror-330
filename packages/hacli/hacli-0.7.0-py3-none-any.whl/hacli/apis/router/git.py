from fastapi import APIRouter, Query

from hacli.apis.schemas.git_models import CreateBranchRequest

router = APIRouter()

from hacli.git import git_ops as git_ops


@router.post(
    "/create/branch",
    description="## 用于在指定的 Git 仓库中创建新分支。\n\n"
                "- `branch` 必须提供，表示新建分支的名称。\n"
                "- `base_branch` 默认值为 `master`，用于指定新分支基于哪个分支。\n"
                "- `is_global` 如果为 `True`，表示在全局 Git 仓库中创建该分支。", )
def create_repo_branch(request: CreateBranchRequest):
    return git_ops.create_local_repo_branch(request.branch, request.base_branch, request.is_global)


@router.post(
    "/create/local/release",
    description="## 用于在本地的 Git 仓库中创建Release分支。\n\n"
                "- `release` 必须提供，表示新建release的名称,如 **25.1.1**。\n")
def create_repo_branch(release: str = Query(
    ...,
    title="Release",
    description="release的名称",
    example="25.1.1",
    min_length=1
), ):
    return git_ops.create_local_release_branch(release)


@router.post(
    "/create/global/rollout_update",
    description="## 用于在Global的 Git 仓库中创建Rollout Update分支。\n\n"
                "- `release` 必须提供，表示新建release的名称,如 **25.1.1**。\n"
                "- `task_id` 必须提供，表示sprint board 上的 task item id,如 **12345**。\n")
def create_repo_branch(
        release: str = Query(
            ...,
            title="Release",
            description="release的名称",
            example="25.1.1",
            min_length=1
        ),
        task_id: str = Query(
            ...,
            title="task_id",
            description="sprint上的task id",
            example="12345",
            min_length=1
        )
):
    return git_ops.create_global_rollout_update_branch(release, task_id)
