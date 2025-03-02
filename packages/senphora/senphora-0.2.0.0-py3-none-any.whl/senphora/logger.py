from loguru import logger
import os

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logger.remove()
logger.add(
    os.path.join(log_dir, "app.log"),
    rotation = '10 MB',
    retention = '5 days',
    level = "DEBUG",
    enqueue=True,
    mode='w',
)