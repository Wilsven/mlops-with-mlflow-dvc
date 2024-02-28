from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    source_url: str
    local_data_file: Path
    unzip_dir: Path
    prefix: str


@dataclass(frozen=True)
class BaseModelConfig:
    root_dir: Path
    base_model_path: Path
    updated_base_model_path: Path
    image_size: list
    learning_rate: float
    include_top: bool
    weights: str
    classes: int


@dataclass(frozen=True)
class ModelTrainerConfig:
    root_dir: Path
    trained_model_file_path: Path
    updated_base_model_path: Path
    data_path: Path
    image_size: list
    epochs: int
    batch_size: int
    augmentation: bool


@dataclass(frozen=True)
class ModelEvaluationConfig:
    root_dir: Path
    model_path: Path
    data_path: Path
    params: dict
    mlflow_uri: str
    image_size: list
    batch_size: int
