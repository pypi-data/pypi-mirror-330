import os
from pathlib import Path

import structlog
from dotenv import load_dotenv
from samgis_core.utilities.session_logger import setup_logging


load_dotenv()
project_root_folder = Path(globals().get("__file__", "./_")).absolute().parent
workdir = Path(os.getenv("WORKDIR", project_root_folder))
static_dist_folder = Path(workdir) / "static" / "dist"
static_dist_folder = Path(os.getenv("FASTAPI_STATIC", static_dist_folder))
model_folder = Path(project_root_folder / "machine_learning_models")

log_level = os.getenv("LOG_LEVEL", "INFO")
setup_logging(log_level=log_level)
app_logger = structlog.stdlib.get_logger()
