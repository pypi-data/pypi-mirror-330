from fastapi import FastAPI

from hacli.apis.core.config import settings
from hacli.apis.router import git, image, tag, deploy, release


def register_router(app: FastAPI):
    """ 注册路由 """
    app.include_router(git.router, prefix=settings.API_PREFIX + "/git", tags=["Git"])
    app.include_router(image.router, prefix=settings.API_PREFIX + "/image", tags=["Image"])
    app.include_router(tag.router, prefix=settings.API_PREFIX + "/tag", tags=["Tag"])
    app.include_router(deploy.router, prefix=settings.API_PREFIX + "/deploy", tags=["Deploy"])
    app.include_router(release.router, prefix=settings.API_PREFIX + "/release", tags=["Release"])
