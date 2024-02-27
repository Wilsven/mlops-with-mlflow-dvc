from cnn_classifier.constants import *
from cnn_classifier.entity.config_entity import (BaseModelConfig,
                                                 DataIngestionConfig,
                                                 ModelTrainerConfig)
from cnn_classifier.utils.common import create_directories, read_yaml


class ConfigurationManager:
    def __init__(
        self,
        config_file_path: Path = CONFIG_FILE_PATH,
        params_file_path: Path = PARAMS_FILE_PATH,
    ):
        """
        Initialize the object with the provided config file path and params file path.

        Args:
            config_file_path (Path): The file path to the configuration file. Defaults to CONFIG_FILE_PATH.
            params_file_path (Path): The file path to the parameters file. Defaults to PARAMS_FILE_PATH.
        """
        self.config = read_yaml(config_file_path)
        self.params = read_yaml(params_file_path)

        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        """
        Returns the data ingestion configuration based on the provided config.

        Returns:
            DataIngestionConfig: The data ingestion configuration object.
        """
        cfg = self.config.data_ingestion

        create_directories([cfg.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=cfg.root_dir,
            source_url=cfg.source_url,
            local_data_file=cfg.local_data_file,
            unzip_dir=cfg.unzip_dir,
            prefix=cfg.prefix,
        )

        return data_ingestion_config

    def get_base_model_config(self) -> BaseModelConfig:
        """
        Returns the base model configuration based on the provided config.

        Returns:
            BaseModelConfig: The base model configuration object.
        """
        cfg = self.config.prepare_base_model
        params = self.params.params

        create_directories([cfg.root_dir])

        base_model_config = BaseModelConfig(
            root_dir=cfg.root_dir,
            base_model_path=cfg.base_model_path,
            updated_base_model_path=cfg.updated_base_model_path,
            image_size=params.IMAGE_SIZE,
            learning_rate=params.LEARNING_RATE,
            include_top=params.INCLUDE_TOP,
            weights=params.WEIGHTS,
            classes=params.CLASSES,
        )

        return base_model_config

    def get_model_trainer_config(self) -> ModelTrainerConfig:
        """
        Return the model trainer configuration based on the provided parameters.

        Returns:
            ModelTrainerConfig: The model trainer configuration object.
        """
        cfg = self.config.model_trainer
        params = self.params.params

        updated_base_model_path = self.config.prepare_base_model.updated_base_model_path
        data_path = [
            f.path
            for f in os.scandir(self.config.data_ingestion.unzip_dir)
            if f.is_dir()
        ][0]

        create_directories([cfg.root_dir])

        model_trainer_config = ModelTrainerConfig(
            root_dir=cfg.root_dir,
            trained_model_file_path=cfg.trained_model_file_path,
            updated_base_model_path=updated_base_model_path,
            data_path=data_path,
            image_size=params.IMAGE_SIZE,
            epochs=params.EPOCHS,
            batch_size=params.BATCH_SIZE,
            augmentation=params.AUGMENTATION,
        )

        return model_trainer_config
