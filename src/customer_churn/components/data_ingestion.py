import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from customer_churn.logger import logger
from customer_churn.exception import CustomException

# ============================================================
# CONFIG
# ============================================================
@dataclass
class DataIngestionConfig:
    raw_data_path: str = os.path.join('artifacts', 'raw.csv')
    train_data_path: str = os.path.join('artifacts', 'train.csv')
    test_data_path: str = os.path.join('artifacts', 'test.csv')


# ============================================================
# COMPONENT
# ============================================================
class DataIngestion:
    def __init__(self):
        self.config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logger.info("Data ingestion started")

        try:
            # -- 1. Read raw data
            source_path = os.path.join('data', 'raw', 'WA_Fn-UseC_-Telco-Customer-Churn.csv')
            df = pd.read_csv(source_path)
            logger.info(f"Dataset loaded — shape: {df.shape}")

            # -- 2. Save raw copy to artifacts
            os.makedirs(os.path.dirname(self.config.raw_data_path), exist_ok=True)
            df.to_csv(self.config.raw_data_path, index=False)
            logger.info(f"Raw data saved to {self.config.raw_data_path}")

            # -- 3. Train/test split (stratified on Churn)
            train_df, test_df = train_test_split(
                df,
                test_size=0.2,
                random_state=42,
                stratify=df['Churn']
            )
            logger.info(f"Train size: {train_df.shape} | Test size: {test_df.shape}")

            # -- 4. Save train and test splits
            train_df.to_csv(self.config.train_data_path, index=False)
            test_df.to_csv(self.config.test_data_path, index=False)
            logger.info(f"Train data saved to {self.config.train_data_path}")
            logger.info(f"Test data saved to {self.config.test_data_path}")

            logger.info("Data ingestion completed successfully")

            return (
                self.config.train_data_path,
                self.config.test_data_path
            )

        except Exception as e:
            raise CustomException(e, sys)


# ============================================================
# ENTRY POINT
# ============================================================
if __name__ == "__main__":
    ingestion = DataIngestion()
    train_path, test_path = ingestion.initiate_data_ingestion()