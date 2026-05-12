import os
import sys
import pandas as pd
import yaml
from dataclasses import dataclass

from customer_churn.logger import logger
from customer_churn.exception import CustomException


# ============================================================
# CONFIG
# ============================================================
@dataclass
class DataValidationConfig:
    validated_data_path: str = os.path.join('artifacts', 'validated.csv')
    schema_path: str = 'schema.yaml'


# ============================================================
# COMPONENT
# ============================================================
class DataValidation:
    def __init__(self):
        self.config = DataValidationConfig()
        self.schema = self._load_schema()

    def _load_schema(self):
        try:
            with open(self.config.schema_path, 'r') as f:
                schema = yaml.safe_load(f)
            logger.info("Schema loaded successfully")
            return schema
        except Exception as e:
            raise CustomException(e, sys)

    def _check_columns(self, df: pd.DataFrame):
        try:
            expected_columns = list(self.schema['columns'].keys())
            missing = [col for col in expected_columns if col not in df.columns]
            extra = [col for col in df.columns if col not in expected_columns]

            if missing:
                raise CustomException(f"Missing columns: {missing}", sys)
            if extra:
                logger.info(f"Extra columns found (will be ignored): {extra}")

            logger.info("Column check passed")

        except CustomException:
            raise
        except Exception as e:
            raise CustomException(e, sys)

    def _check_dtypes(self, df: pd.DataFrame):
        try:
            mismatches = []
            for col, expected_dtype in self.schema['columns'].items():
                if col in df.columns:
                    actual_dtype = str(df[col].dtype)
                    if actual_dtype != expected_dtype:
                        mismatches.append(
                            f"{col}: expected {expected_dtype}, got {actual_dtype}"
                        )

            if mismatches:
                logger.info(f"Dtype mismatches (transformation will fix): {mismatches}")
            else:
                logger.info("Dtype check passed")

        except Exception as e:
            raise CustomException(e, sys)

    def _check_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            duplicate_count = df.duplicated().sum()

            if duplicate_count > 0:
                df = df.drop_duplicates()
                logger.info(f"Dropped {duplicate_count} duplicate rows — new shape: {df.shape}")
            else:
                logger.info("No duplicates found")

            return df

        except Exception as e:
            raise CustomException(e, sys)

    def _check_nulls(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            # standard nulls
            null_counts = df.isnull().sum()
            cols_with_nulls = null_counts[null_counts > 0]

            if cols_with_nulls.empty:
                logger.info("No null values found")
            else:
                before = df.shape[0]
                df = df.dropna()
                logger.info(f"Dropped {before - df.shape[0]} null rows — new shape: {df.shape}")

            # hidden spaces in TotalCharges
            hidden = df[df['TotalCharges'].str.strip() == '']
            if len(hidden) > 0:
                before = df.shape[0]
                df = df[df['TotalCharges'].str.strip() != '']
                logger.info(f"Dropped {before - df.shape[0]} hidden space rows in TotalCharges — new shape: {df.shape}")
            else:
                logger.info("No hidden spaces found in TotalCharges")

            return df

        except Exception as e:
            raise CustomException(e, sys)

    def _check_target_values(self, df: pd.DataFrame):
        try:
            expected_values = self.schema['expected_churn_values']
            actual_values = df['Churn'].unique().tolist()
            unexpected = [val for val in actual_values if val not in expected_values]

            if unexpected:
                raise CustomException(
                    f"Unexpected values in Churn column: {unexpected}", sys
                )
            logger.info("Target column check passed — Churn has only Yes/No values")

        except CustomException:
            raise
        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_validation(self, raw_data_path: str):
        logger.info("Data validation started")

        try:
            df = pd.read_csv(raw_data_path)
            logger.info(f"Data loaded for validation — shape: {df.shape}")

            self._check_columns(df)
            self._check_dtypes(df)
            df = self._check_duplicates(df)
            df = self._check_nulls(df)
            self._check_target_values(df)

            os.makedirs(os.path.dirname(self.config.validated_data_path), exist_ok=True)
            df.to_csv(self.config.validated_data_path, index=False)
            logger.info(f"Validated data saved to {self.config.validated_data_path}")
            logger.info("Data validation completed successfully")

            return self.config.validated_data_path

        except Exception as e:
            raise CustomException(e, sys)


# ============================================================
# ENTRY POINT
# ============================================================
if __name__ == "__main__":
    validation = DataValidation()
    validated_path = validation.initiate_data_validation(
        raw_data_path=os.path.join('artifacts', 'raw.csv')
    )