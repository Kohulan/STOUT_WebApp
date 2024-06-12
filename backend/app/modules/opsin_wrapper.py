from __future__ import annotations
import os
from typing import List, Union
import pystow
from jpype import (
    getDefaultJVMPath,
    isJVMStarted,
    JClass,
    JPackage,
    JVMNotFoundException,
    startJVM,
)
from rdkit import Chem
import pandas as pd
from app.modules.visualize_wrapper import get_svg_2d


def setup_jvm():
    try:
        jvmPath = getDefaultJVMPath()
    except JVMNotFoundException:
        print("If you see this message, for some reason JPype cannot find jvm.dll.")
        print(
            "This indicates that the environment variable JAVA_HOME is not set properly."
        )
        print("You can set it or set it manually in the code")
        jvmPath = "Define/path/or/set/JAVA_HOME/variable/properly"

    if not isJVMStarted():
        paths = {
            "opsin-cli-2.8.0-jar-with-dependencies": "https://github.com/dan2097/opsin/releases/download/2.8.0/opsin-cli-2.8.0-jar-with-dependencies.jar"
        }

        jar_paths = {
            key: str(pystow.join("STOUT-V2")) + f"/{key}.jar" for key in paths.keys()
        }
        for key, url in paths.items():
            if not os.path.exists(jar_paths[key]):
                pystow.ensure("STOUT-V2", url=url)

        startJVM("-ea", "-Xmx4096M", classpath=[jar_paths[key] for key in jar_paths])
        print(jar_paths)


setup_jvm()
opsin_base = JPackage("uk").ac.cam.ch.wwmm.opsin
_nametostruct = opsin_base.NameToStructure.getInstance()
_restoinchi = opsin_base.NameToInchi.convertResultToInChI


def get_smiles_opsin(input_text: str) -> str:
    """Convert IUPAC chemical name to SMILES notation using OPSIN.

    Parameters:
    - input_text (str): The IUPAC chemical name to be converted.

    Returns:
    - str: The SMILES notation corresponding to the given IUPAC name.

    Raises:
    - Exception: If the IUPAC name is not valid or if there are issues in the conversion process. The exception message will guide the user to check the data again.
    """
    try:
        # print(input_text)
        OpsinResult = _nametostruct.parseChemicalName(input_text)
        # print(OpsinResult)
        if str(OpsinResult.getStatus()) == "FAILURE":
            raise Exception(
                (
                    "Failed to convert '%s' to format '%s'\n%s using OPSIN"
                    % (input_text, format, OpsinResult.getMessage())
                ),
            )
        # print(OpsinResult.getSmiles())
        return str(OpsinResult.getSmiles())
    except Exception:
        return str(
            "Failed to convert '%s' to format '%s'\n%s using OPSIN"
            % (input_text, format, OpsinResult.getMessage()),
        )


def generate_inchi_from_smiles(smiles: str) -> str:
    """Generate an InChI from a given SMILES string.

    Args:
        smiles (str): The SMILES string of the molecule.

    Returns:
        str: The generated InChI.
    """
    # Convert SMILES string to RDKit Mol object
    mol = Chem.MolFromSmiles(smiles)

    # Check if the molecule is valid
    if mol is None:
        raise ValueError("Invalid SMILES string.")

    # Generate InChI
    inchi = Chem.MolToInchi(mol)

    return inchi


def process_predicted_smiles(
    smiles: str, predicted_IUPAC: str, retranslate: bool = True, visualize: bool = False
) -> str:
    """
    Process predicted IUPAC name into SMILES representation.

    Args:
        smiles (str): The original SMILES representation.
        predicted_IUPAC (str): The predicted IUPAC name.

    Returns:
        str: A formatted string containing the processed data.
             The string format is "<original_smiles>,<predicted_IUPAC>,<success_status>,<translated_smiles>".

    Notes:
        - If OPSIN restranslation is successful, the success_status is "True", and translated_smiles contains the SMILES representation.
        - If restranslation fails, the success_status is "False", and translated_smiles is the string "Failed to retranslate".
    """
    predicted_smiles = get_smiles_opsin(predicted_IUPAC.replace(";", " "))

    if "Failed to convert" not in predicted_smiles:
        if generate_inchi_from_smiles(smiles) == generate_inchi_from_smiles(
            predicted_smiles
        ):
            if visualize:
                if retranslate:
                    return f"{smiles}\t{get_svg_2d(smiles)}\t{predicted_IUPAC}\tsame as input\t{predicted_smiles}\t{get_svg_2d(smiles)}"
                else:
                    return f"{smiles}\t{get_svg_2d(smiles)}\t{predicted_IUPAC}"
            else:
                if retranslate:
                    return f"{smiles}\t{predicted_IUPAC}\tsame as input\t{predicted_smiles}"
                else:
                    return f"{smiles}\t{predicted_IUPAC}"

        else:
            # Translation successful but wrong molecule
            if visualize:
                if retranslate:
                    return f"{smiles}\t{get_svg_2d(smiles)}\t{predicted_IUPAC}\tnot same as input\t{predicted_smiles}\t{get_svg_2d(predicted_smiles)}"
                else:
                    return f"{smiles}\t{get_svg_2d(smiles)}\t{predicted_IUPAC}"
            else:
                if retranslate:
                    return f"{smiles}\t{predicted_IUPAC}\tnot same as input\t{predicted_smiles}"
                else:
                    return f"{smiles}\t{predicted_IUPAC}"
    else:
        # Translation failed
        if visulaize:
            return f"{smiles}\t{get_svg_2d(smiles)}\t{predicted_IUPAC}\tunable to assess\tfailed to retranslate"
        else:
            return (
                f"{smiles}\t{predicted_IUPAC}\tunable to assess\tfailed to retranslate"
            )


def convert_to_table(data: list) -> pd.DataFrame:
    """
    Convert a list of strings into a DataFrame representing a table.

    Args:
        data (list): A list of strings where each string represents a row of the table.

    Returns:
        pd.DataFrame: A DataFrame representing the table.
    """
    # Split each string into columns based on comma separator and convert to DataFrame
    df = pd.DataFrame([row.split("\t") for row in data])

    # Set the first row as column names
    df.columns = df.iloc[0]

    # Remove the first row (header row)
    df = df[1:]

    return df


def get_opsin_convertion(
    iupac_list: list, retranslate: bool = True, visualize: bool = False
) -> pd.DataFrame:
    """
    Convert a list of IUPAC names into SMILES representations using Open Parser for Systematic IUPAC Nomenclature (OPSIN).

    Args:
        iupac_list (list): A list of SMILES, IUPAC names.

    Returns:
        pd.DataFrame: A DataFrame representing the processed data with columns:
                      "Original SMILES", "Predicted IUPAC name", "Retranslation", "Retranslated SMILES".

    Notes:
        - Each item in iupac_list is expected to be a tab-separated string containing the original SMILES and
          predicted IUPAC name.
        - The function iterates through each entry in the iupac_list, processes it using the process_predicted_smiles
          function, and collects the processed data in a list.
        - The first entry in the returned list is the header row.
    """
    # Initialize the list to store processed data
    all_iupac = []

    if visualize:
        if retranslate:
            # Append header row
            all_iupac.append(
                "Original SMILES\tOriginal Structure\tPredicted IUPAC name\tRetranslated Structure\tRetranslated SMILES\tRetranslated Structure"
            )
        else:
            all_iupac.append(
                "Original SMILES\tOriginal Structure\tPredicted IUPAC name"
            )
    else:
        if retranslate:
            # Append header row
            all_iupac.append(
                "Original SMILES\tPredicted IUPAC name\tRetranslated Structure\tRetranslated SMILES"
            )
        else:
            all_iupac.append("Original SMILES\tPredicted IUPAC name")

    # Iterate through each entry in iupac_list
    for entry in iupac_list:
        # Process each entry and append to the result list
        processed_entry = process_predicted_smiles(
            *entry.split("\t"), retranslate, visualize
        )
        all_iupac.append(processed_entry)

    return convert_to_table(all_iupac)
