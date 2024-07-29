import tensorflow as tf
from rdkit import Chem
import pickle
import re
import pystow
import os
import zipfile

# Set path
default_path = pystow.join("STOUT-V2", "models")

# model download location
model_url = "https://storage.googleapis.com/decimer_weights/models.zip"
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


def load_model():
    inp_lang = pickle.load(
        open(default_path.as_posix() + "/assets/tokenizer_input.pkl", "rb")
    )

    targ_lang = pickle.load(
        open(default_path.as_posix() + "/assets/tokenizer_target.pkl", "rb")
    )

    inp_max_length = 602
    reloaded = tf.saved_model.load(default_path.as_posix() + "/translator_forward")

    return inp_lang, targ_lang, inp_max_length, reloaded


inp_lang, targ_lang, inp_max_length, reloaded = load_model()


def preprocess_sentence(w: str) -> str:
    """Preprocesses a sentence by adding start and end tokens, and spacing punctuation.

    Args:
        w (str): Input sentence.

    Returns:
        str: Preprocessed sentence.
    """
    w = "<start> " + w + " <end>"
    return w


def tokenize_input(sentence_input: str) -> tf.Tensor:
    """Tokenizes the input sentence using the pre-trained tokenizer and pads the sequence to a fixed length.

    Args:
        sentence_input (str): Input sentence.

    Returns:
        tf.Tensor: Tokenized and padded input sequence.
    """
    sentence = preprocess_sentence(sentence_input)
    inputs = [inp_lang.word_index[i] for i in sentence.split(" ")]
    inputs_ = tf.keras.preprocessing.sequence.pad_sequences(
        [inputs], maxlen=inp_max_length, padding="post"
    )

    return inputs_


def detokenize_output(predicted_array: tf.Tensor) -> str:
    """Detokenizes the predicted output sequence into a string representation.

    Args:
        predicted_array (tf.Tensor): Predicted output sequence.

    Returns:
        str: Detokenized output string.
    """
    outputs = [targ_lang.index_word[i] for i in predicted_array[0].numpy()]
    prediction = (
        "".join([str(elem) for elem in outputs])
        .replace("§", " ")
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
    decoded = tokenize_input(x_can)
    result = reloaded(tf.constant(decoded))
    prediction = detokenize_output(result)
    return prediction
