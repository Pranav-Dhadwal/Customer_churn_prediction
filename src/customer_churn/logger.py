import logging
import os
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
LOG_PATH = os.path.join(os.getcwd(), "logs")
os.makedirs(LOG_PATH, exist_ok=True)
LOG_FILE_PATH = os.path.join(LOG_PATH, LOG_FILE)

LOG_FORMAT = (
    "============================================================\n"
    "TIME     : %(asctime)s\n"
    "LEVEL    : %(levelname)s\n"
    "MODULE   : %(name)s\n"
    "LINE     : %(lineno)d\n"
    "MESSAGE  : %(message)s\n"
    "============================================================"
)

# root logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# -- file handler (saves to logs/)
file_handler = logging.FileHandler(LOG_FILE_PATH)
file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

# -- stream handler (prints to terminal)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter(LOG_FORMAT))

logger.addHandler(file_handler)
logger.addHandler(stream_handler)