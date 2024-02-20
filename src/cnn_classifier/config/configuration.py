from cnn_classifier.constants import *
from cnn_classifier.entity.config_entity import DataIngestionConfig
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
