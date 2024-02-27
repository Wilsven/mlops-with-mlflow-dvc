from pathlib import Path
from typing import Optional

import tensorflow as tf

from cnn_classifier.entity.config_entity import BaseModelConfig


class PrepareBaseModel:
    def __init__(self, config: BaseModelConfig):
        """
        Initializes the class with the given BaseModelConfig object.

        Args:
            config (BaseModelConfig): The configuration object for base model.
        """
        self.config = config

    def get_base_model(self):
        """Returns the base model for the given configuration."""
        self.model = tf.keras.applications.vgg16.VGG16(
            input_shape=self.config.image_size,
            weights=self.config.weights,
            include_top=self.config.include_top,
        )

        self.save_model(path=self.config.base_model_path, model=self.model)

    def update_base_model(self):
        """Updates the base model with the prepared full model with additional parameters."""
        self.full_model = self._prepare_full_model(
            model=self.model,
            classes=self.config.classes,
            freeze_all=True,
            freeze_till=None,
            learning_rate=self.config.learning_rate,
        )

        self.save_model(path=self.config.updated_base_model_path, model=self.full_model)

    @staticmethod
    def save_model(path: Path, model: tf.keras.Model):
        """
        Saves the given `tf.keras.Model` to the specified path.

        Args:
            path (Path): The path where the model will be saved.
            model (tf.keras.Model): The model to be saved.
        """
        model.save(path)

    @staticmethod
    def _prepare_full_model(
        model: tf.keras.Model,
        classes: int,
        freeze_all: bool = True,
        freeze_till: Optional[int] = None,
        learning_rate: float = 0.01,
    ) -> tf.keras.Model:
        """
        Prepares a full model by freezing specified layers, adding a flatten layer,
        a dense prediction layer, compiling the model, and returning the full model.

        Args:
            model (tf.keras.Model): The input model.
            classes (int): The number of output classes.
            freeze_all (bool, optional): Whether to freeze all layers. Defaults to True.
            freeze_till (Optional[int], optional): Number of layers to freeze from the end. Defaults to None.
            learning_rate (float, optional): Learning rate for the optimizer. Defaults to 0.01.

        Returns:
            tf.keras.Model: The compiled full model.
        """
        if freeze_all:
            model.trainable = False
        elif (freeze_till is not None) and (freeze_till > 0):
            for layer in model.layers[:-freeze_till]:
                layer.trainable = False

        flatten_in = tf.keras.layers.Flatten()(model.output)
        prediction = tf.keras.layers.Dense(units=classes, activation="softmax")(
            flatten_in
        )

        full_model = tf.keras.models.Model(inputs=model.input, outputs=prediction)
        full_model.compile(
            optimizer=tf.keras.optimizers.legacy.SGD(learning_rate=learning_rate),
            loss=tf.keras.losses.CategoricalCrossentropy(),
            metrics=["accuracy"],
        )
        full_model.summary()

        return full_model
