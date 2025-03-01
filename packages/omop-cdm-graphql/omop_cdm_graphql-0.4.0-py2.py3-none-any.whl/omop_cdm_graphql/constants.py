import logging
import os

from datetime import datetime

DEFAULT_PROJECT = "omop-cdm-graphql"

DEFAULT_TIMESTAMP = str(datetime.today().strftime("%Y-%m-%d-%H%M%S"))

DEFAULT_OUTDIR_BASE = os.path.join(
    "/tmp/",
    os.getenv("USER"),
    DEFAULT_PROJECT,
)

DEFAULT_LOGGING_FORMAT = (
    "%(levelname)s : %(asctime)s : %(pathname)s : %(lineno)d : %(message)s"
)

DEFAULT_LOGGING_LEVEL = logging.INFO

DEFAULT_VERBOSE = False

DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 8080
DEFAULT_DATABASE_FILE = "omop_cdm.db"
