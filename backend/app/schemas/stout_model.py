from pydantic import BaseModel
from pydantic import Field


class STOUTOutputModel(BaseModel):
    """
    Model for the STOUT output.

    This class defines the structure for storing the output data from STOUT.

    Attributes:
        data (List): A list containing the output data from STOUT processing.

    """

    data: list


class STOUTtableModel(BaseModel):
    """Represents a data model for the STOUT processed table.

    Attributes:
        table_data (dict): A converted dictionary representing the processed data with their values.
    """

    table_data: dict = Field(
        ...,
        title="STOUT conversion data",
        description="A converted dictionary representing the processed data with columns: Original SMILES, Predicted IUPAC name, Retranslation, Retranslated SMILES.",
    )

    class Config:
        """Pydantic model configuration.

        JSON Schema Extra:
        - Includes examples of the response structure.
        """

        json_schema_extra = {
            "examples": [
                {
                    "input": "CN1C=NC2=C1C(=O)N(C(=O)N2C)C\nCC1(C)OC2COC3(COS(N)(=O)=O)OC(C)(C)OC3C2O1",
                    "message": "Success",
                    "output": "STOUT output as a JSON",
                },
            ],
        }


class GenerateSMILESResponse(BaseModel):
    """Represents a response containing a generated SMILES string and depiction.

    Properties:
    - smiles (str): The generated SMILES string.
    - depiction (str): The depiction (2D or 3D) corresponding to the generated SMILES string.
    """

    smiles: str = Field(
        ...,
        title="SMILES",
        description="The generated SMILES string corresponding to the input text.",
    )
    depiction: str = Field(
        ...,
        title="Depiction",
        description="The depiction (2D or 3D) corresponding to the generated SMILES string.",
    )

    class Config:
        """Pydantic model configuration.

        JSON Schema Extra:
        - Includes examples of the response structure.
        """

        json_schema_extra = {
            "examples": [
                {
                    "input": "1,3,7-trimethylpurine-2,6-dione",
                    "message": "Success",
                    "output": {
                        "smiles": "CN1C=NC2=C1C(=O)N(C)C(=O)N2C",
                        "depiction": "<svg>...</svg>",
                    },
                },
            ],
        }
