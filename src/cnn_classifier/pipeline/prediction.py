import os

import numpy as np

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image


class PredictionPipeline:

    def __init__(self, file_name: str):
        """
        Initializes the class with the given file name.

        Args:
            file_name (str): The name of the file.
        """
        self.file_name = file_name

    def predict(self) -> list:
        """
        A method to make a prediction using a trained model and return the prediction result.

        Returns:
            list: List of dictionary containing the prediction.
        """
        # Load the model
        model = load_model(os.path.join("model", "trained_model.keras"))

        image_name = self.file_name
        test_image = image.load_img(image_name, target_size=(224, 224))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)
        result = np.argmax(model.predict(test_image), axis=1)
        print(result)

        return (
            [{"image": "Normal"}]
            if result[0] == 1
            else [{"image": "Adenocarcinoma Cancer"}]
        )
