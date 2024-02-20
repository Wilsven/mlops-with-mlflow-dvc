import base64
import json
import os
from pathlib import Path
from typing import Any

import joblib
import yaml
from box import ConfigBox
from box.exceptions import BoxValueError
from ensure import ensure_annotations

from cnn_classifier import logger


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """
    Reads the given YAML file and loads into a ConfigBox object.

    Args:
        path_to_yaml (Path): Path to load YAML file from.

    Raises:
        ValueError: Raises error if YAML file is empty.
        e: Exception.

    Returns:
        ConfigBox: A ConfigBox object containing the data loaded as class attributes.
    """
    try:
        with open(path_to_yaml) as f:
            content = yaml.safe_load(f)
            logger.info(f"Loaded YAML file successfully from: {path_to_yaml}")

            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("YAML file is empty")
    except Exception as e:
        raise e


@ensure_annotations
def create_directories(path_to_directories: list, verbose: bool = True):
    """
    Ensures that the given directories are created, from a list of paths.

    Args:
        path_to_directories (list): The list of paths to create directories for.
        verbose (bool, optional): Whether to display verbose output. Defaults to True.
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"Created directory at: {path}")


@ensure_annotations
def save_json(path: Path, data: dict):
    """
    Saves JSON data to the specified file path.

    Args:
        path (Path): The file path where the JSON data will be saved.
        data (dict): The JSON data to be saved.
    """
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

    logger.info(f"JSON file saved at: {path}")


@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """
    Loads a JSON file from the given path and return the content as a ConfigBox.

    Args:
        path (Path): The path to the JSON file.

    Returns:
        ConfigBox: The content of the JSON file wrapped in a
        ConfigBox where data is loaded as class attributes.
    """
    with open(path) as f:
        content = json.load(f)

    logger.info(f"JSON file loaded succesfully from: {path}")

    return ConfigBox(content)


@ensure_annotations
def save_bin(data: Any, path: Path):
    """
    Saves binary data to a file.

    Args:
        data (Any): The data to be saved.
        path (Path): The file path where the data will be saved.
    """
    joblib.dump(value=data, filename=path)
    logger.info(f"Binary file saved at: {path}")


@ensure_annotations
def load_bin(path: Path) -> Any:
    """
    Loads a binary file from the given path and return the loaded data.

    Args:
        path (Path): The path to the binary file.

    Returns:
        Any: The loaded data from the binary file.
    """
    data = joblib.load(path)
    logger.info(f"Binary file loaded from: {path}")

    return data


@ensure_annotations
def get_size(path: Path) -> str:
    """
    A function to get the size of a file at the specified path and return it in kilobytes.

    Parameters:
    path (Path): The path to the file

    Returns:
    str: The size of the file in kilobytes
    """
    size_in_kb = round(os.path.getsize(path) / 1024)

    return f"~ {size_in_kb} KB"


def decode_image(img_str: str, file_name: str):
    """
    Decodes the base64 encoded image string and writes the resulting image data to a file.

    Args:
        img_str (str): The base64 encoded image string.
        file_name (str): The name of the file to write the image data to.
    """
    img_data = base64.b64decode(img_str)
    with open(file_name, "wb") as f:
        f.write(img_data)


def encode_image(img_path: str) -> str:
    """
    Encodes an image file to base64.

    Args:
        img_path (str): The file path of the image to encode.

    Returns:
        str: The base64 encoded string representing the image.
    """
    with open(img_path, "rb") as f:
        return base64.b64encode(f.read())
