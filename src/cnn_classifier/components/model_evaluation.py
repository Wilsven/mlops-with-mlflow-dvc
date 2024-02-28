import os
from pathlib import Path
from urllib.parse import urlparse

import mlflow
import mlflow.keras
import tensorflow as tf

from cnn_classifier.entity.config_entity import ModelEvaluationConfig
from cnn_classifier.utils.common import save_json


class ModelEvaluation:

    def __init__(self, config: ModelEvaluationConfig):
        """
        Initializes the class with the given ModelEvaluationConfig object.

        Parameters:
            config (ModelEvaluationConfig): The configuration object for model evaluation.
        """
        self.config = config

    def _val_generator(self):
        """
        Generates the validation data generator for the model.
        """
        data_generator_kwargs = dict(rescale=1 / 255, validation_split=0.30)
        data_flow_kwargs = dict(
            target_size=self.config.image_size[:-1],
            batch_size=self.config.batch_size,
            interpolation="bilinear",
        )

        val_data_generator = tf.keras.preprocessing.image.ImageDataGenerator(
            **data_generator_kwargs
        )

        self.val_generator = val_data_generator.flow_from_directory(
            directory=self.config.data_path,
            subset="validation",
            shuffle=False,
            **data_flow_kwargs,
        )

    @staticmethod
    def load_model(path: Path) -> tf.keras.Model:
        """
        Loads a Keras model from the given path.

        Args:
            path (Path): The path to the model file.

        Returns:
            tf.keras.Model: The loaded Keras model.
        """
        return tf.keras.models.load_model(path)

    def evaluation(self):
        """
        Method to perform evaluation using the loaded model and validation data generator.
        """
        self.model = self.load_model(self.config.model_path)
        self._val_generator()
        self.score = self.model.evaluate(self.val_generator)

    def save_score(self, path: Path, scores: dict):
        """
        Saves the scores to a specified file path in JSON format.

        Args:
            path (Path): The file path where the scores will be saved.
            scores (dict): A dictionary containing the loss and accuracy to be saved.
        """
        save_json(path, data=scores)

    def log_into_mlflow(self):
        """
        Sets the MLflow registry URI, starts a new MLflow run, logs parameters and metrics,
        saves scores locally, and registers the model in MLflow Model Registry if the tracking
        URI scheme is not "file". Otherwise, logs the model without registering it.
        """
        mlflow.set_registry_uri(self.config.mlflow_uri)
        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

        with mlflow.start_run():
            scores = {"loss": self.score[0], "accuracy": self.score[1]}
            mlflow.log_params(self.config.params)
            mlflow.log_metrics(scores)

            # Get run id
            run = mlflow.active_run()
            run_id = run.info.run_id
            # Save scores locally as well
            path = os.path.join(self.config.root_dir, f"scores_{run_id}.json")
            self.save_score(Path(path), scores)

            # Model registry does not work with file store
            if tracking_url_type_store != "file":
                # Register the model
                # There are other ways to use the Model Registry, which depends on the use case,
                # please refer to the doc for more information:
                # https://mlflow.org/docs/latest/model-registry.html#api-workflow
                mlflow.keras.log_model(
                    self.model, "model", registered_model_name="VGG16Model"
                )
            else:
                mlflow.keras.log_model(self.model, "model")
