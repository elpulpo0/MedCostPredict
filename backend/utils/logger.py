from loguru import logger
from pathlib import Path
import sys


def setup_logger(level="INFO", log_dir=None, log_name=None):
    if log_dir is None:
        log_dir = Path(__file__).resolve().parents[2] / "logs"

    log_dir.mkdir(parents=True, exist_ok=True)

    log_path = log_dir / f"{log_name}.log"

    logger.remove()
    logger.add(
        log_path,
        rotation="1 MB",
        level=level,
        format="<level>{time:DD-MM-YYYY HH:mm:ss} | {level} | {message}</level>",
    )
    logger.add(
        sys.stdout,
        level=level,
        format="<level>{time:DD-MM-YYYY HH:mm:ss} | {level} | {message}</level>",
    )

    return logger
