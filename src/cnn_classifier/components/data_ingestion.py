import os
import zipfile

import gdown

from cnn_classifier import logger
from cnn_classifier.entity.config_entity import DataIngestionConfig


class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        """
        Initializes the class with the given DataIngestionConfig object.

        Args:
            config (DataIngestionConfig): The configuration object for data ingestion.
        """
        self.config = config

    def download_data(self):
        """
        Downloads the data from a specified source URL and save it to a local file.

        Parameters:
            self: The instance of the class.
        """
        try:
            root_dir = self.config.root_dir
            source_url = self.config.source_url
            local_data_file = self.config.local_data_file
            os.makedirs(root_dir, exist_ok=True)
            logger.info(
                f"Downloading data from {source_url} into file {local_data_file}"
            )

            file_id = source_url.split("/")[-2]
            prefix = self.config.prefix
            gdown.download(f"{prefix}{file_id}", local_data_file)
            logger.info(
                f"Downloaded data from {source_url} into file {local_data_file}"
            )

        except Exception as e:
            logger.error(f"Failed to download data: {e}")
            raise e

    def extract_zip_file(self):
        """
        Extracts a zip file into the specified directory.

        Parameters:
            self (object): The object instance
            unzip_dir (str): The directory to extract the zip file into
        """
        unzip_dir = self.config.unzip_dir
        os.makedirs(unzip_dir, exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file, "r") as f:
            f.extractall(unzip_dir)
            logger.info(
                f"Extracted data from {self.config.local_data_file} into {unzip_dir}"
            )
