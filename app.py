import os

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS, cross_origin

from cnn_classifier.pipeline.prediction import PredictionPipeline
from cnn_classifier.utils.common import decode_image

os.putenv("LANG", "en_US.UTF-8")
os.putenv("LC_ALL", "en_US.UTF-8")


app = Flask(__name__)
CORS(app)


class Client:
    def __init__(self):
        self.file_name = "input_image.jpg"
        self.classifier = PredictionPipeline(self.file_name)


client = Client()


@app.route("/", methods=["GET"])
@cross_origin()
def index():
    return render_template("index.html")


@app.route("/train", methods=["GET", "POST"])
@cross_origin()
def train():
    os.system("python main.py")
    # os.system("dvc repro")
    return "Training completed successfully"


@app.route("/predict", methods=["POST"])
@cross_origin()
def predict():
    image = request.json["image"]
    file_name = client.file_name
    decode_image(image, file_name)
    result = client.classifier.predict()
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)  # local host
