from customer_churn.logger import logging
from customer_churn.exception import CustomException
import sys


logging.info("Logger test started")

try:
    a = 1 / 0

except Exception as e:
    logging.info("Custom exception triggered")
    raise CustomException(e, sys)