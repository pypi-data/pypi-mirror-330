import os
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

logger.info("Loading DETOXAI...")


# Only if the environment variables are not set
if "DETOXAI_ROOT_PATH" not in os.environ:
    DETOXAI_ROOT_PATH = Path(os.path.expanduser("~")) / ".detoxai"
    print(f"DETOXAI_ROOT_PATH: {DETOXAI_ROOT_PATH}")
    os.environ["DETOXAI_ROOT_PATH"] = str(DETOXAI_ROOT_PATH)

if "DETOXAI_DATASET_PATH" not in os.environ:
    DETOXAI_ROOT_PATH = Path(os.environ["DETOXAI_ROOT_PATH"])
    DETOXAI_DATASET_PATH = DETOXAI_ROOT_PATH / "datasets"
    os.environ["DETOXAI_DATASET_PATH"] = str(DETOXAI_DATASET_PATH)

logger.info(f'Detoxai paths: {os.getenv("DETOXAI_ROOT_PATH")}, {os.getenv("DETOXAI_DATASET_PATH")}')

from .datasets.catalog.download import download_datasets  # noqa
from .core.interface import debias  # noqa

import importlib.metadata

try:
    __version__ = importlib.metadata.version(__package__ or __name__)
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"
