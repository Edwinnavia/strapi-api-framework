import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime


def setup_logger(name="strapi_framework", log_dir="logs", level=logging.INFO):
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, f"{datetime.now().strftime('%Y-%m-%d')}.log")

    log_format = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(log_format, datefmt=date_format)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        file_handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=5, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger


if __name__ == "__main__":
    logger = setup_logger("strapi_api")
    logger.info("Logger configured correctly for Strapi Framework.")
