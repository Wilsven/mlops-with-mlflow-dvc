from cnn_classifier import logger
from cnn_classifier.components.model_trainer import ModelTrainer
from cnn_classifier.config.configuration import ConfigurationManager


class ModelTrainerPipeline:

    def run_pipeline(self):
        """
        Method to run the base model trainer pipeline.

        Raises:
            e: Exception.
        """
        try:
            logger.info("Model training started")
            configuration_manager = ConfigurationManager()
            model_trainer_config = configuration_manager.get_model_trainer_config()
            model_trainer = ModelTrainer(config=model_trainer_config)
            model_trainer.get_base_model()
            model_trainer.train_val_generator()
            model_trainer.train()
            logger.info("Model training ended")

        except Exception as e:
            logger.error(f"Model training failed: {e}")
            raise e
