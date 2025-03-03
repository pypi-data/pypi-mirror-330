from fastapi import FastAPI
from rich import print
from starlette.requests import Request
from starlette.responses import JSONResponse


def register_exception(app: FastAPI):
    @app.exception_handler(Exception)
    async def exception_handler(request: Request, exc: Exception):
        print(f"[red]An unexpected error occurred: {str(exc)}[/red]")
        return JSONResponse(
            status_code=500,
            content={"message": f"An unexpected error occurred: {str(exc)}"},
        )
