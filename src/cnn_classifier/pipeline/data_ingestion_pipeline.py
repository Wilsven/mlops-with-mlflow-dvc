from cnn_classifier import logger
from cnn_classifier.components.data_ingestion import DataIngestion
from cnn_classifier.config.configuration import ConfigurationManager


class DataIngestionPipeline:

    def run_pipeline(self, configuration_manager: ConfigurationManager):
        """
        Method to run the data ingestion pipeline.

        Args:
            configuration_manager (ConfigurationManager): The configuration manager object.

        Raises:
            e: Exception.
        """
        try:
            logger.info("Data ingestion started")
            data_ingestion_config = configuration_manager.get_data_ingestion_config()
            data_ingestion = DataIngestion(config=data_ingestion_config)
            data_ingestion.download_data()
            data_ingestion.extract_zip_file()
            logger.info("Data ingestion completed")

        except Exception as e:
            logger.error(f"Data ingestion failed: {e}")
            raise e


if __name__ == "__main__":
    data_ingestion_pipeline = DataIngestionPipeline()
    data_ingestion_pipeline.run_pipeline(configuration_manager=ConfigurationManager())
