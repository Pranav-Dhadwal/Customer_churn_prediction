"""
template.py
-----------
Script to automatically generate the structure of project

Usage:
    python template.py
"""

import os
import logging
from pathlib import Path

# == Logging == 
logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(message)s")

# == File manifest == 
# Directories and new files will be created automatically if not present

PROJECT_NAME = "Churn_predic"

files = [
    # Package init files
    f"src/__init__.py",
    f"src/{PROJECT_NAME}/__init__.py",
    f"src/{PROJECT_NAME}/components/__init__.py",
    f"src/{PROJECT_NAME}/pipelines/__init__.py",

    # Core utilities
    f"src/{PROJECT_NAME}/logger.py",
    f"src/{PROJECT_NAME}/exception.py",
    f"src/{PROJECT_NAME}/utils.py",

    # Pipeline components
    f"src/{PROJECT_NAME}/components/data_ingestion.py",
    f"src/{PROJECT_NAME}/components/data_transformation.py",
    f"src/{PROJECT_NAME}/components/model_trainer.py",
    f"src/{PROJECT_NAME}/components/model_monitoring.py",

    # Pipelines
    f"src/{PROJECT_NAME}/pipelines/training_pipeline.py",
    f"src/{PROJECT_NAME}/pipelines/prediction_pipeline.py",

    # Project root files
    "requirements.txt",
    "setup.py",
    ".env",
    ".gitignore",

    # Data directories (keep them tracked by git via .gitkeep)
    "data/raw/.gitkeep",
    "data/processed/.gitkeep",
    "logs/.gitkeep",
    "artifacts/.gitkeep",
    "notebooks/eda.ipynb",
]

# == Script == 
for filepath in files:
    path = Path(filepath)

    # Create parent directories if they don't exist
    path.parent.mkdir(parents=True, exist_ok=True)

    # Create the file only if it doesn't already exist
    if not path.exists():
        path.touch()
        logging.info(f"Created  : {path}")
    else:
        logging.info(f"Skipped  : {path}  (already exists)")

logging.info("✅  Project structure ready.")