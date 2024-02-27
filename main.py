from cnn_classifier.pipeline.data_ingestion_pipeline import DataIngestionPipeline
from cnn_classifier.pipeline.model_trainer_pipeline import ModelTrainerPipeline
from cnn_classifier.pipeline.prepare_base_model_pipeline import PrepareBaseModelPipeline


def run_pipelines(
    data_ingestion_pipeline: DataIngestionPipeline,
    prepare_base_model_pipeline: PrepareBaseModelPipeline,
    model_trainer_pipeline: ModelTrainerPipeline,
):
    """
    Runs the entire pipeline.

    Args:
        data_ingestion_pipeline (DataIngestionPipeline): The data ingestion pipeline object.
        prepare_base_model_pipeline (PrepareBaseModelPipeline): The prepare base model pipeline object.
        model_trainer_pipeline (ModelTrainerPipeline): The model trainer pipeline object.
    """
    data_ingestion_pipeline.run_pipeline()
    prepare_base_model_pipeline.run_pipeline()
    model_trainer_pipeline.run_pipeline()


if __name__ == "__main__":
    # Instantiate pipelines
    data_ingestion_pipeline = DataIngestionPipeline()
    prepare_base_model_pipeline = PrepareBaseModelPipeline()
    model_trainer_pipeline = ModelTrainerPipeline()

    # Run all pipelines
    run_pipelines(
        data_ingestion_pipeline, prepare_base_model_pipeline, model_trainer_pipeline
    )
