import tensorflow as tf
from rdkit import Chem
import pickle
import re
import pystow
import os
import zipfile
import numpy as np

# Set path
default_path = pystow.join("STOUT-V2", "models")

# model download location
model_url = "https://zenodo.org/records/12542360/files/models.zip?download=1"
model_path = str(default_path) + "/translator_forward/"


# Downloads the model and unzips the file downloaded, if the model is not present on the working directory.
def download_trained_weights(model_url: str, model_path: str, verbose=1):
    """This function downloads the trained models and tokenizers to a default location.
    After downloading the zipped file the function unzips the file automatically.
    If the model exists on the default location this function will not work.

    Args:
        model_url (str): trained model url for downloading.
        model_path (str): model default path to download.

    Returns:
        downloaded model.
    """
    # Download trained models
    if verbose > 0:
        print("Downloading trained model to " + str(model_path))
        model_path = pystow.ensure("STOUT-V2", url=model_url)
        print(model_path)
    if verbose > 0:
        print("... done downloading trained model!")
        with zipfile.ZipFile(model_path.as_posix(), "r") as zip_ref:
            zip_ref.extractall(model_path.parent.as_posix())


# download models to a default location
if not os.path.exists(model_path):
    download_trained_weights(model_url, default_path)


def load_model_forward():
    """
    Load the forward translation model along with the required tokenizers.

    This function loads the input and target tokenizers used for translating
    SMILES to IUPAC names, along with the saved forward translation model.

    Returns:
        tuple: A tuple containing:
            - inp_lang (Tokenizer): The tokenizer for the input language (SMILES).
            - targ_lang (Tokenizer): The tokenizer for the target language (IUPAC names).
            - inp_max_length (int): The maximum length of the input sequences.
            - reloaded (tf.Module): The loaded TensorFlow model for forward translation.
    """
    inp_lang = pickle.load(
        open(default_path.as_posix() + "/assets/tokenizer_input.pkl", "rb")
    )

    targ_lang = pickle.load(
        open(default_path.as_posix() + "/assets/tokenizer_target.pkl", "rb")
    )

    inp_max_length = 602
    reloaded = tf.saved_model.load(default_path.as_posix() + "/translator_forward")

    return inp_lang, targ_lang, inp_max_length, reloaded


def load_model_backward():
    """
    Load the backward translation model along with the required tokenizers.

    This function loads the input and target tokenizers used for translating
    IUPAC names to SMILES, along with the saved backward translation model.

    Returns:
        tuple: A tuple containing:
            - inp_lang (Tokenizer): The tokenizer for the input language (IUPAC names).
            - targ_lang (Tokenizer): The tokenizer for the target language (SMILES).
            - inp_max_length (int): The maximum length of the input sequences.
            - reloaded (tf.Module): The loaded TensorFlow model for backward translation.
    """
    targ_lang = pickle.load(
        open(default_path.as_posix() + "/assets/tokenizer_input.pkl", "rb")
    )

    inp_lang = pickle.load(
        open(default_path.as_posix() + "/assets/tokenizer_target.pkl", "rb")
    )

    inp_max_length = 1002
    reloaded = tf.saved_model.load(default_path.as_posix() + "/translator_reverse")

    return inp_lang, targ_lang, inp_max_length, reloaded


(
    inp_lang_forward,
    targ_lang_forward,
    inp_max_length_forward,
    reloaded_forward,
) = load_model_forward()
(
    inp_lang_backward,
    targ_lang_backward,
    inp_max_length_backward,
    reloaded_backward,
) = load_model_backward()


def preprocess_sentence(w: str) -> str:
    """Preprocesses a sentence by adding start and end tokens, and spacing punctuation.

    Args:
        w (str): Input sentence.

    Returns:
        str: Preprocessed sentence.
    """
    w = "<start> " + w + " <end>"
    return w


def tokenize_input(input_SMILES: str, inp_lang, inp_max_length: int) -> np.array:
    """This function takes a user input SMILES and tokenizes it
       to feed it to the model.

    Args:
        input_SMILES (string): SMILES string given by the user.
        inp_lang: keras_preprocessing.text.Tokenizer object with input language.
        inp_max_length: maximum number of characters in the input language.

    Returns:
        tokenized_input (np.array): The SMILES get split into meaningful chunks
        and gets converted into meaningful tokens. The tokens are arrays.
    """
    sentence = preprocess_sentence(input_SMILES)
    inputs = [inp_lang.word_index[i] for i in sentence.split(" ")]
    tokenized_input = tf.keras.preprocessing.sequence.pad_sequences(
        [inputs], maxlen=inp_max_length, padding="post"
    )

    return tokenized_input


def detokenize_output_forward(predicted_array: tf.Tensor) -> str:
    """Detokenizes the predicted output sequence into a string representation.

    Args:
        predicted_array (tf.Tensor): Predicted output sequence.

    Returns:
        str: Detokenized output string.
    """
    outputs = [targ_lang_forward.index_word[i] for i in predicted_array[0].numpy()]
    prediction = (
        "".join([str(elem) for elem in outputs])
        .replace("<start>", "")
        .replace("<end>", "")
    )
    return prediction


def detokenize_output_backward(predicted_array: tf.Tensor) -> str:
    """Detokenizes the predicted output sequence into a string representation.

    Args:
        predicted_array (tf.Tensor): Predicted output sequence.

    Returns:
        str: Detokenized output string.
    """
    outputs = [targ_lang_backward.index_word[i] for i in predicted_array[0].numpy()]
    prediction = (
        "".join([str(elem) for elem in outputs])
        .replace("<start>", "")
        .replace("<end>", "")
    )
    return prediction


def split_character(SMILES: str) -> str:
    """Takes user input, splits it into characters, and generates tokens.

    Args:
        SMILES (str): User input SMILES.

    Returns:
        str: Tokenized SMILES.
    """
    SMILES = SMILES.replace("\\/", "/")
    mol = Chem.MolFromSmiles(SMILES, sanitize=False)
    if mol:
        smiles = Chem.MolToSmiles(mol, kekuleSmiles=True)
        splitted_list = list(smiles)
        tokenized_SMILES = re.sub(
            r"\s+(?=[a-z])", "", " ".join(map(str, splitted_list))
        )
        return tokenized_SMILES


def predict_IUPAC(smiles: str) -> str:
    """Predicts the IUPAC name given a SMILES string.

    Args:
        smiles (str): Input SMILES string.

    Returns:
        str: Predicted IUPAC name.
    """
    x_can = split_character(smiles)
    decoded = tokenize_input(x_can, inp_lang_forward, inp_max_length_forward)
    result = reloaded_forward(tf.constant(decoded))
    prediction = detokenize_output_forward(result)
    return prediction


def predict_SMILES(smiles: str) -> str:
    """Predicts the IUPAC name given a SMILES string.

    Args:
        smiles (str): Input IUPAC name.

    Returns:
        str: Predicted SMILES string.
    """
    x_can = split_character(smiles)
    decoded = tokenize_input(x_can)
    result = reloaded_backward(tf.constant(decoded))
    prediction = detokenize_output_backward(result)
    return prediction
