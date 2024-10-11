from __future__ import annotations
import os

from typing import Literal, Optional
from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel

from app.schemas.healthcheck import HealthCheck
from app.modules.decimer_wrapper import get_decimer
from app.modules.visualize_wrapper import get_svg_2d, get_html_3d
from app.schemas.error import BadRequestModel, NotFoundModel, ErrorResponse

router = APIRouter(
    prefix="/decimer",
    tags=["decimer"],
    dependencies=[],
    responses={
        200: {"description": "OK"},
        400: {"description": "Bad Request", "model": BadRequestModel},
        404: {"description": "Not Found", "model": NotFoundModel},
        422: {"description": "Unprocessable Entity", "model": ErrorResponse},
    },
)


class DECIMEROutputModel(BaseModel):
    SMILES: str
    Depiction: Optional[str] = None


@router.post(
    "/image2SMILES",
    summary="Use DECIMER to translate chemical structure images into SMILES",
    responses={
        200: {
            "description": "Successful response",
            "model": DECIMEROutputModel,
        },
        400: {"description": "Bad Request", "model": BadRequestModel},
        404: {"description": "Not Found", "model": NotFoundModel},
        422: {"description": "Unprocessable Entity", "model": ErrorResponse},
    },
)
async def decimer_image_to_smiles(
    file: UploadFile = File(...),
    visualize: Optional[Literal["2D", "3D"]] = Query(
        None, description="Optional visualization type"
    ),
):
    """
    Generate SMILES from a given chemical structure image using DECIMER.

    Parameters:
    - **file**: required (UploadFile): The image file containing the chemical structure.
    - **visualize**: optional (str): If provided, visualize the generated SMILES in 2D or 3D.

    Returns:
    - DECIMEROutputModel: Contains the SMILES string and its depiction (if visualization was requested).
    """
    try:
        # Save the uploaded file temporarily
        temp_file_path = f"temp_{file.filename}"
        with open(temp_file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        # Process the image with DECIMER
        smiles = get_decimer(temp_file_path)

        # Generate depiction if visualization was requested
        depiction = None
        if visualize == "2D":
            depiction = get_svg_2d(smiles)
        elif visualize == "3D":
            depiction = get_html_3d(smiles)

        # Remove the temporary file
        os.remove(temp_file_path)

        return DECIMEROutputModel(SMILES=smiles, Depiction=depiction)

    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))
