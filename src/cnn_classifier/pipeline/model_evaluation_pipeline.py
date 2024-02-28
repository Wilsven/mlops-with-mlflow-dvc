from cnn_classifier import logger
from cnn_classifier.components.model_evaluation import ModelEvaluation
from cnn_classifier.config.configuration import ConfigurationManager


class ModelEvaluationPipeline:

    def run_pipeline(self, configuration_manager: ConfigurationManager):
        """
        Method to run the model evaluation pipeline.

        Args:
            configuration_manager (ConfigurationManager): The configuration manager object.

        Raises:
            e: Exception.
        """
        try:
            logger.info("Model evaluation started")
            model_evaluation_config = (
                configuration_manager.get_model_evaluation_config()
            )
            model_evaluation = ModelEvaluation(config=model_evaluation_config)
            model_evaluation.evaluation()
            # model_evaluation.log_into_mlflow()  # only for production
            logger.info("Model evaluation ended")

        except Exception as e:
            logger.error(f"Model evaluation failed: {e}")
            raise e


if __name__ == "__main__":
    model_evaluation_pipeline = ModelEvaluationPipeline()
    model_evaluation_pipeline.run_pipeline(configuration_manager=ConfigurationManager())
