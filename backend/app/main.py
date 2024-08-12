from __future__ import annotations

import os

from fastapi import FastAPI
from fastapi import status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi_versioning import VersionedFastAPI

# from prometheus_fastapi_instrumentator import Instrumentator

from .routers import stout
from app.exception_handlers import input_exception_handler
from app.exception_handlers import InvalidInputException
from app.schemas.healthcheck import HealthCheck

app = FastAPI(
    title="STOUT API Microservice",
    description="STOUT (SMILES-TO-IUPAC-name translator), a deep-learning neural machine translation approach to generate the IUPAC name for a given molecule from its SMILES string.",
    # terms_of_service="https://docs.api.naturalproducts.net",
    contact={
        "name": "Kohulan Rajan",
        "url": "https://cheminf.uni-jena.de/",
        "email": "kohulan.rajan@uni-jena.de",
    },
    license_info={
        "name": "CC BY 4.0",
        "url": "https://creativecommons.org/licenses/by/4.0/",
    },
)

app.include_router(stout.router)


app = VersionedFastAPI(
    app,
    version_format="{major}",
    prefix_format="/v{major}",
    enable_latest=True,
    # terms_of_service="https://docs.api.naturalproducts.net",
    contact={
        "name": "Kohulan Rajan",
        "url": "https://cheminf.uni-jena.de/",
        "email": "kohulan.rajan@uni-jena.de",
    },
    license_info={
        "name": "CC BY 4.0",
        "url": "https://creativecommons.org/licenses/by/4.0/",
    },
    version=os.getenv("RELEASE_VERSION", "1.0"),
)


origins = ["*"]


@app.middleware("http")
async def add_cors_headers(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# register exception handlers
for sub_app in app.routes:
    if hasattr(sub_app.app, "add_exception_handler"):
        sub_app.app.add_exception_handler(
            InvalidInputException,
            input_exception_handler,
        )


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url=os.getenv("HOMEPAGE_URL", "/latest/docs"))


@app.get(
    "/health",
    tags=["healthcheck"],
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
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
