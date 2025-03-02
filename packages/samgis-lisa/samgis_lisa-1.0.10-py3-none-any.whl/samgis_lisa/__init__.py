"""Get machine learning predictions from geodata raster images"""
import os

import structlog.stdlib
from pathlib import Path

from samgis_core.utilities import session_logger
from samgis_web.utilities.constants import SERVICE_NAME


ROOT = Path(globals().get("__file__", "./_")).absolute().parent.parent
PROJECT_ROOT_FOLDER = Path(os.getenv("PROJECT_ROOT_FOLDER", ROOT))

loglevel = os.getenv('LOGLEVEL', 'INFO').upper()
session_logger.setup_logging(log_level=loglevel)
app_logger = structlog.stdlib.get_logger(__name__)
