from loguru import logger

from config.splitted_settings.boilerplate import BASE_DIR

logger.add(f"{BASE_DIR}/logs/in_data.log", filter=lambda record: record["extra"]["task"] == "write_in_data")
logger.add(f"{BASE_DIR}/logs/out_data.log", filter=lambda record: record["extra"]["task"] == "write_out_data")
logger.add(f"{BASE_DIR}/logs/app.log", filter=lambda record: record["extra"]["task"] == "app")
