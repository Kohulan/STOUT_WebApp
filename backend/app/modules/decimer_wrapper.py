import tensorflow as tf
import numpy as np
from typing import List
import app.modules.config as config
import pickle

with open("app/modules/assets/tokenizer_new2023.pkl", "rb") as f:
    tokenizer = pickle.load(f)

# Pre-compute index_word dictionary for faster lookup
index_word = tokenizer.index_word
start_token = "<start>"
end_token = "<end>"


def detokenize_output(predicted_array: np.ndarray) -> str:
    """
    Convert predicted array of tokens to a SMILES string.

    Args:
        predicted_array (np.ndarray): Transformer Decoder output array (predicted tokens)

    Returns:
        str: SMILES string
    """
    outputs = np.vectorize(lambda i: index_word.get(i, ""))(predicted_array[0])
    return "".join(outputs).replace(start_token, "").replace(end_token, "")


def load_tflite_model(model_path: str) -> tf.lite.Interpreter:
    """
    Load a TFLite model and allocate tensors.

    Args:
        model_path (str): Path to the TFLite model file

    Returns:
        tf.lite.Interpreter: Loaded TFLite interpreter
    """
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    return interpreter


def predict_smiles(interpreter: tf.lite.Interpreter, image: np.ndarray) -> str:
    """
    Predict SMILES string from an image using the given TFLite model.

    Args:
        interpreter (tf.lite.Interpreter): Loaded TFLite interpreter
        image (np.ndarray): Input image

    Returns:
        str: Predicted SMILES string
    """
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    interpreter.set_tensor(input_details[0]["index"], np.array(image, dtype=np.float32))

    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]["index"])

    return detokenize_output(output_data)


interpreter = load_tflite_model("app/modules/assets/DECIMER_model.tflite")


def get_decimer(image_path: str):
    # Process the image

    image = config.decode_image(image_path)

    # Predict SMILES
    smiles = predict_smiles(interpreter, image)

    return smiles
