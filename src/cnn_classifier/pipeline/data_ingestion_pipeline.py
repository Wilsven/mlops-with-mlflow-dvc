from cnn_classifier import logger
from cnn_classifier.components.data_ingestion import DataIngestion
from cnn_classifier.config.configuration import ConfigurationManager


class DataIngestionPipeline:

    def run_pipeline(self):
        """
        Method to run the data ingestion pipeline.

        Raises:
            e: Exception.
        """
        try:
            logger.info("Data ingestion started")
            configuration_manager = ConfigurationManager()
            data_ingestion_config = configuration_manager.get_data_ingestion_config()
            data_ingestion = DataIngestion(config=data_ingestion_config)
            data_ingestion.download_data()
            data_ingestion.extract_zip_file()
            logger.info("Data ingestion completed")

        except Exception as e:
            logger.error(f"Data ingestion failed: {e}")
            raise e
