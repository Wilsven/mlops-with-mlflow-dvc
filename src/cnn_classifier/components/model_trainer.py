from pathlib import Path

import tensorflow as tf

from cnn_classifier.entity.config_entity import ModelTrainerConfig


class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        """
        Initializes the class with the given ModelTrainerConfig object.

        Parameters:
            config (ModelTrainerConfig): The configuration object for the model training.
        """
        self.config = config

    def get_base_model(self):
        """
        Gets the base model and loads it using the updated base model path from the configuration.
        """
        self.model = tf.keras.models.load_model(self.config.updated_base_model_path)

    def train_val_generator(self):
        """
        Generates the training and validation data generators for the model.
        """
        data_generator_kwargs = dict(rescale=1 / 255, validation_split=0.20)
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

        if self.config.augmentation:
            train_data_generator = tf.keras.preprocessing.image.ImageDataGenerator(
                rotation_range=40,
                horizontal_flip=True,
                width_shift_range=0.2,
                height_shift_range=0.2,
                shear_range=0.2,
                zoom_range=0.2,
                **data_generator_kwargs,
            )
        else:
            train_data_generator = val_data_generator

        self.train_generator = train_data_generator.flow_from_directory(
            directory=self.config.data_path,
            subset="training",
            shuffle=True,
            **data_flow_kwargs,
        )

    @staticmethod
    def save_model(path: Path, model: tf.keras.Model):
        """
        Saves the provided Keras model to the given path.

        Parameters:
            path (Path): The file path where the model will be saved.
            model (tf.keras.Model): The Keras model to be saved.
        """
        model.save(path)

    def train(self):
        """
        Trains the model using the train and validation generators and saves the trained model to a specified path.
        """
        self.steps_per_epoch = (
            self.train_generator.samples // self.train_generator.batch_size
        )
        self.validation_steps = (
            self.val_generator.samples // self.val_generator.batch_size
        )

        self.model.fit(
            self.train_generator,
            epochs=self.config.epochs,
            steps_per_epoch=self.steps_per_epoch,
            validation_steps=self.validation_steps,
            validation_data=self.val_generator,
        )

        self.save_model(path=self.config.trained_model_file_path, model=self.model)
