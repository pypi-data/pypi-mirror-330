from typing import Optional, List

from fastapi.params import Query
from pydantic import BaseModel


class DeployRequest(BaseModel):
    release: str  # 发布版本号
    product_names: Optional[List[str]] = Query(None, alias="products", description="要部署的产品名称列表，可指定多个")
    deploy_all_product: bool = False  # 是否部署所有产品
