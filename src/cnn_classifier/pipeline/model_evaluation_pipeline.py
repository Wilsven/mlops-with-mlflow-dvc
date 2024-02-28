from cnn_classifier import logger
from cnn_classifier.components.model_evaluation import ModelEvaluation
from cnn_classifier.config.configuration import ConfigurationManager


class ModelEvaluationPipeline:

    def run_pipeline(self):
        """
        Method to run the model evaluation pipeline.

        Raises:
            e: Exception.
        """
        try:
            logger.info("Model evaluation started")
            configuration_manager = ConfigurationManager()
            model_evaluation_config = (
                configuration_manager.get_model_evaluation_config()
            )
            model_evaluation = ModelEvaluation(config=model_evaluation_config)
            model_evaluation.evaluation()
            model_evaluation.log_into_mlflow()
            logger.info("Model evaluation ended")

        except Exception as e:
            logger.error(f"Model evaluation failed: {e}")
            raise e
