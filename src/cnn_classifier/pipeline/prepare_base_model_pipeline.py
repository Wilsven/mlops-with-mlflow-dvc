from cnn_classifier import logger
from cnn_classifier.components.prepare_base_model import PrepareBaseModel
from cnn_classifier.config.configuration import ConfigurationManager


class PrepareBaseModelPipeline:

    def run_pipeline(self, configuration_manager: ConfigurationManager):
        """
        Method to run the base model preparation pipeline.

        Args:
            configuration_manager (ConfigurationManager): The configuration manager object.

        Raises:
            e: Exception.
        """
        try:
            logger.info("Base model preparation started")
            base_model_config = configuration_manager.get_base_model_config()
            prepare_base_model = PrepareBaseModel(config=base_model_config)
            prepare_base_model.get_base_model()
            prepare_base_model.update_base_model()
            logger.info("Base model preparation completed")

        except Exception as e:
            logger.error(f"Base model preparation failed: {e}")
            raise e


if __name__ == "__main__":
    prepare_base_model_pipeline = PrepareBaseModelPipeline()
    prepare_base_model_pipeline.run_pipeline(
        configuration_manager=ConfigurationManager()
    )
