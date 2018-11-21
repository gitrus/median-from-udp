import logging.handlers
import os
from pathlib import Path

ENDPOINT_HOST = os.environ.get("ENDPOINT_HOST")
ENDPOINT_PORT = os.environ.get("ENDPOINT_PORT")

PG_HOST = os.environ.get("PG_HOST")
PG_PORT = os.environ.get("PG_PORT")
PG_USER = os.environ.get("PG_USER")
PG_PASSWORD = os.environ.get("PG_PASSWORD")


SEQUENCE_DUMP_NUMBER = 100 * 60

REPO_DIR = Path(__file__).parent.parent.parent


def setup_logging(
    path_to_log_file: str = f'{REPO_DIR}/log.log',
    max_bytes: int = 100 * 1024 * 1024,
    backup_count: int = 5,
) -> logging.Logger:
    logger = logging.getLogger('info_log')
    logger.setLevel(logging.INFO)

    handler = logging.handlers.RotatingFileHandler(
        path_to_log_file,
        maxBytes=max_bytes,
        backupCount=backup_count
    )
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter('%(asctime)s %(process)d %(levelno)s %(message)s'))
    logger.addHandler(handler)

    return logger
