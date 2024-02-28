from cnn_classifier.config.configuration import ConfigurationManager
from cnn_classifier.pipeline.data_ingestion_pipeline import DataIngestionPipeline
from cnn_classifier.pipeline.model_evaluation_pipeline import ModelEvaluationPipeline
from cnn_classifier.pipeline.model_trainer_pipeline import ModelTrainerPipeline
from cnn_classifier.pipeline.prepare_base_model_pipeline import PrepareBaseModelPipeline


pipelines = {
    "data_ingestion_pipeline": DataIngestionPipeline(),
    "prepare_base_model_pipeline": PrepareBaseModelPipeline(),
    "model_trainer_pipeline": ModelTrainerPipeline(),
    "model_evaluation_pipeline": ModelEvaluationPipeline(),
}


def run_pipelines(configuration_manager: ConfigurationManager):
    """
    Runs the entire pipeline.

    Args:
        configuration_manager (ConfigurationManager): The configuration manager object to generat the configurations.
    """
    for pipeline_name in pipelines:
        # Get the pipeline using the name
        pipeline = pipelines[pipeline_name]
        pipeline.run_pipeline(configuration_manager=configuration_manager)


if __name__ == "__main__":
    # Instantiate the configuration manager once
    configuration_manager = ConfigurationManager()

    # # Run all pipelines
    run_pipelines(configuration_manager)
