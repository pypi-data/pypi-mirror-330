import json

from fastapi import APIRouter

from lisa_on_cuda import app_logger


router = APIRouter()


@router.get("/health")
def health() -> str:
    try:
        from samgis_core.__version__ import __version__ as version_core
        from gradio import __version__ as gradio_version

        app_logger.info(f"still alive, gradio_version:{gradio_version}, version_core:{version_core}.")
        return json.dumps({"msg": "lisa on cuda: still alive..."})
    except Exception as e:
        app_logger.error(f"exception:{e}.")
        return json.dumps({"msg": "request failed"})
