import typer
from rich import print
from rich.prompt import Confirm
from typing_extensions import Any

from ..tag.get_global_rollout_status import get_global_rollout_status
from ..utils.ado import execute_pipeline

app = typer.Typer()


# TODO ... not include shared services images
@app.command(name="import_global_service_images")
def import_global_service_images() -> dict[str, Any]:
    if not Confirm.ask(
            "Are you sure to trigger pipeline to import service images, have you checked service images imported?"): return

    rollout_tags: dict[str, str] = get_global_rollout_status()

    res = {}
    for product, tag in rollout_tags.items():
        pipeline = execute_pipeline(release="master",
                                    pipeline_name_env_key="DEPLOY_PIPELINES_IMPORT_GLOBAL_SERVICE_IMAGES_NAME",
                                    pipeline_parameter_env_key="DEPLOY_PIPELINES_IMPORT_GLOBAL_SERVICE_IMAGES_PARAMETERS",
                                    project_name_env_key="PROJECT_GLOBAL_NAME",
                                    project_repo_env_key="PROJECT_GLOBAL_REPO", product=product, tag=tag)
        res[product] = pipeline

    print(res)
    return res
