from cnn_classifier import logger
from cnn_classifier.components.prepare_base_model import PrepareBaseModel
from cnn_classifier.config.configuration import ConfigurationManager


class PrepareBaseModelPipeline:

    def run_pipeline(self):
        """
        Method to run the base model preparation pipeline.

        Raises:
            e: Exception.
        """
        try:
            logger.info(f"Prepare base model started")
            configuration_manager = ConfigurationManager()
            base_model_config = configuration_manager.get_base_model_config()
            prepare_base_model = PrepareBaseModel(config=base_model_config)
            prepare_base_model.get_base_model()
            prepare_base_model.update_base_model()

        except Exception as e:
            logger.error(f"Prepare base model failed: {e}")
            raise e
