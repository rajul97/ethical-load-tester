# src/logger.py
import logging
from config import LOG_FILE  # ✅ Correct

def setup_logger(log_file):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    return logging.getLogger("LoadTester")

logger = setup_logger(LOG_FILE)  # ✅ Now LOG_FILE is defined
