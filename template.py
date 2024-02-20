import logging
import os
from pathlib import Path

PROJECT_NAME = "cnn_classifier"
FILE_PATHS = [
    ".github/workflows/.gitkeep",
    "Dockerfile",
    "app.py",
    "config/config.yaml",
    "dvc.yaml",
    "main.py",
    "params.yaml",
    "requirements.txt",
    "research/01_data_ingestion.ipynb",
    "research/02_prepare_base_model.ipynb",
    "research/03_model_trainer.ipynb",
    "research/04_model_evaluation.ipynb",
    "research/trials.ipynb",
    "schema.yaml",
    "setup.py",
    f"src/{PROJECT_NAME}/__init__.py",
    f"src/{PROJECT_NAME}/components/__init__.py",
    f"src/{PROJECT_NAME}/components/data_ingestion.py",
    f"src/{PROJECT_NAME}/components/prepare_base_model.py",
    f"src/{PROJECT_NAME}/components/model_trainer.py",
    f"src/{PROJECT_NAME}/components/model_evaluation.py",
    f"src/{PROJECT_NAME}/config/__init__.py",
    f"src/{PROJECT_NAME}/config/configuration.py",
    f"src/{PROJECT_NAME}/constants/__init__.py",
    f"src/{PROJECT_NAME}/entity/__init__.py",
    f"src/{PROJECT_NAME}/entity/config_entity.py",
    f"src/{PROJECT_NAME}/pipeline/__init__.py",
    f"src/{PROJECT_NAME}/pipeline/data_ingestion_pipeline.py",
    f"src/{PROJECT_NAME}/pipeline/prepare_base_model_pipeline.py",
    f"src/{PROJECT_NAME}/pipeline/model_trainer_pipeline.py",
    f"src/{PROJECT_NAME}/pipeline/model_evaluation_pipeline.py",
    f"src/{PROJECT_NAME}/utils/__init__.py",
    f"src/{PROJECT_NAME}/utils/common.py",
    "templates/index.html",
]


def create_project_structure():

    for file_path in FILE_PATHS:
        file_path = Path(file_path)
        file_dir, file_name = os.path.split(file_path)

        if len(file_dir) != 0:
            os.makedirs(file_dir, exist_ok=True)
            logging.info(f"Creating directory: {file_dir}")

        # If file does not exist, create it
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            with open(file_path, "w") as f:
                logging.info(f"Creating file: {file_name}")
                pass

        else:
            logging.info(
                f"File {file_name} already exists in file directory {file_dir}"
            )


if __name__ == "__main__":
    create_project_structure()
    logging.info("Project structure created successfully")
