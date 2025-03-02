from pydantic import BaseModel, Field


class CreateBranchRequest(BaseModel):
    branch: str = Field(..., description="新分支的名称", example="feature/new-branch")
    base_branch: str = Field("master", description="基础分支名称", example="develop")
    is_global: bool = Field(False, description="是否在全局 Git 仓库中创建分支", example=True)
