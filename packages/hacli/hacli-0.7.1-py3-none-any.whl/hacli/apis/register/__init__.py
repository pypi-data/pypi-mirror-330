from fastapi import FastAPI

from .exception import register_exception


def register(app: FastAPI):
    register_exception(app)
