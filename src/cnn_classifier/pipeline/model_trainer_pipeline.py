from cnn_classifier import logger
from cnn_classifier.components.model_trainer import ModelTrainer
from cnn_classifier.config.configuration import ConfigurationManager


class ModelTrainerPipeline:

    def run_pipeline(self, configuration_manager: ConfigurationManager):
        """
        Method to run the base model trainer pipeline.

        Args:
            configuration_manager (ConfigurationManager): The configuration manager object.

        Raises:
            e: Exception.
        """
        try:
            logger.info("Model training started")
            model_trainer_config = configuration_manager.get_model_trainer_config()
            model_trainer = ModelTrainer(config=model_trainer_config)
            model_trainer.get_base_model()
            model_trainer.train_val_generator()
            model_trainer.train()
            logger.info("Model training ended")

        except Exception as e:
            logger.error(f"Model training failed: {e}")
            raise e


if __name__ == "__main__":
    model_trainer_pipeline = ModelTrainerPipeline()
    model_trainer_pipeline.run_pipeline(configuration_manager=ConfigurationManager())
