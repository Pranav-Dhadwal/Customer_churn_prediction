import logging
import os
from datetime import datetime


LOG_FILE = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"

LOG_PATH = os.path.join(os.getcwd(), "logs")
os.makedirs(LOG_PATH, exist_ok=True)

LOG_FILE_PATH = os.path.join(LOG_PATH, LOG_FILE)


LOG_FORMAT = """
============================================================
TIME     : %(asctime)s
LEVEL    : %(levelname)s
MODULE   : %(name)s
LINE     : %(lineno)d
MESSAGE  : %(message)s
============================================================
"""


logging.basicConfig(
    filename=LOG_FILE_PATH,
    format=LOG_FORMAT,
    level=logging.INFO
)