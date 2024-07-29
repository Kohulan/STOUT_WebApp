from __future__ import annotations

import io
from typing import Literal
from typing import Union

from fastapi import APIRouter
from fastapi import Body
from fastapi import HTTPException
from fastapi import Query
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.responses import Response

from rdkit import Chem
from app.schemas import HealthCheck
from app.schemas.stout_model import (
    STOUTtableModel,
    STOUTOutputModel,
    GenerateSMILESResponse,
)
from app.modules.opsin_wrapper import get_opsin_convertion, get_smiles_opsin
from app.modules import predict_IUPAC
from app.modules.visualize_wrapper import get_svg_2d, get_html_3d
from app.schemas.error import BadRequestModel
from app.schemas.error import ErrorResponse
from app.schemas.error import NotFoundModel
from STOUT import translate_reverse

router = APIRouter(
    prefix="/stout",
    tags=["stout"],
    dependencies=[],
    responses={
        200: {"description": "OK"},
        400: {"description": "Bad Request", "model": BadRequestModel},
        404: {"description": "Not Found", "model": NotFoundModel},
        422: {"description": "Unprocessable Entity", "model": ErrorResponse},
    },
)


@router.get("/", include_in_schema=False)
@router.get(
    "/health",
    tags=["healthcheck"],
    summary="Perform a Health Check on Chem Module",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
    response_model=HealthCheck,
)
def get_health() -> HealthCheck:
    """## Perform a Health Check.

    Endpoint to perform a health check on. This endpoint can primarily be used by Docker
    to ensure a robust container orchestration and management are in place. Other
    services that rely on the proper functioning of the API service will not deploy if this
    endpoint returns any other HTTP status code except 200 (OK).
    Returns:
            HealthCheck: Returns a JSON response with the health status
    """
    return HealthCheck(status="OK")


@router.post(
    "/SMILE2IUPAC",
    summary="Use STOUT to translate SMILES into IUPAC names",
    responses={
        200: {
            "description": "Successful response",
            "model": Union[STOUTOutputModel, STOUTtableModel],
        },
        400: {"description": "Bad Request", "model": BadRequestModel},
        404: {"description": "Not Found", "model": NotFoundModel},
        422: {"description": "Unprocessable Entity", "model": ErrorResponse},
    },
)
async def stout_molecules(
    smiles_list: str = Body(
        embed=False,
        media_type="text/plain",
        openapi_examples={
            "example1": {
                "summary": "Example: SMILES",
                "value": "CN1C=NC2=C1C(=O)N(C(=O)N2C)C\nCC1(C)OC2COC3(COS(N)(=O)=O)OC(C)(C)OC3C2O1",
            },
        },
    ),
    retranslate: bool = Query(
        False,
        title="Retranslate(OPSIN)",
        description="Retranslate the predicted IUPAC names using OPSIN",
    ),
    format: Literal["json", "html"] = Query(
        default=lambda: "html", description="Desired display format"
    ),
):
    all_iupac = []
    all_data = []
    for item in io.StringIO(smiles_list):
        smiles = item.strip()
        mol = Chem.MolFromSmiles(smiles)
        if mol:
            predicted_IUPAC = predict_IUPAC(smiles)
            all_iupac.append(predicted_IUPAC)
            all_data.append(smiles + "\t" + predicted_IUPAC)
    if retranslate:
        if format == "html":
            table_data = get_opsin_convertion(all_data, visualize=True)
            with open("app/templates/style.css", "r") as file:
                css_style = file.read()
            html_table = table_data.to_html(index=False)
            return Response(content=css_style + html_table, media_type="text/html")
        else:
            table_data = get_opsin_convertion(all_data)
            return JSONResponse(content=table_data.to_json())
    elif format == "html":
        table_data = get_opsin_convertion(all_data, retranslate=False, visualize=True)
        with open("app/templates/style.css", "r") as file:
            css_style = file.read()
        html_table = table_data.to_html(index=False)
        return Response(content=css_style + html_table, media_type="text/html")
    elif format == "json":
        table_data = get_opsin_convertion(all_data, retranslate=False)
        return JSONResponse(content=table_data.to_json())
    else:
        return all_iupac


@router.get(
    "/IUPAC2SMILES",
    summary="Generate SMILES from a given input",
    responses={
        200: {
            "description": "Successful response",
            "model": GenerateSMILESResponse,
        },
        400: {"description": "Bad Request", "model": BadRequestModel},
        404: {"description": "Not Found", "model": NotFoundModel},
        422: {"description": "Unprocessable Entity", "model": ErrorResponse},
    },
)
async def iupac_name_to_smiles(
    input_text: str = Query(
        title="Input IUPAC name",
        description="IUPAC name of the molecule",
        openapi_examples={
            "example1": {
                "summary": "Example: IUPAC name",
                "value": "1,3,7-trimethylpurine-2,6-dione",
            },
        },
    ),
    converter: Literal["opsin", "stout"] = Query(
        default="opsin",
        description="Required type of converter for IUPAC",
    ),
    visualize: Literal["2D", "3D"] = Query(
        default="2D",
        description="Visualize the Generate SMILES in 2D/3D",
    ),
):
    """Generate SMILES from a given IUPAC name or a SELFIES representation.

    Parameters:
    - **input_text**: required (str): The input text containing the IUPAC names.

    Notes:
    - The IUPAC name should follow the standard IUPAC naming conventions for organic compounds.

    Example Usage:
    - To generate SMILES from an IUPAC name: /IUPAC2SMILES?input_text=benzene
    """
    try:
        if converter == "opsin":
            smiles = get_smiles_opsin(input_text)
        else:
            smiles = translate_reverse(input_text)
        if smiles:
            if visualize == "2D":
                depiction = get_svg_2d(smiles)
            elif visualize == "3D":
                depiction = get_html_3d(smiles)

            return {"SMILES": str(smiles), "Depiction": depiction}
        else:
            return str(smiles)

    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))
