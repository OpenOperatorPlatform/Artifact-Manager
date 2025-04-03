from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from . import schemas
from src.skopeo.skopeo import SkopeoClient

app = FastAPI(
    title="Artifact Manager API",
    description="WIP API for managing artifacts using Skopeo.",
    version="0.1.0",
    openapi_tags=[
        {
            "name": "Artifact Management",
            "description": (
                "Operations related to artifact management in container "
                "registries."
            )
        }
    ]
)


@app.get("/", include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse(url="/docs")


@app.post("/image-exists", tags=["Artifact Management"])
def image_exists(
    artifact: schemas.PostImageExists
) -> schemas.PostImageExistsResponse:
    # Return type annotation for the endpoint
    """
    API endpoint to check if a Helm Chart or container image with a specific
    tag exists in a repository.
    """
    try:
        exists = SkopeoClient.image_exists(
            registry_url=artifact.registry_url,
            image_name=artifact.image_name,
            image_tag=artifact.image_tag,
            username=artifact.username,
            password=artifact.password
        )
        return schemas.PostImageExistsResponse(exists=exists)

    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Uncategorized error: " + str(e)
        )


@app.post("/copy-image", tags=["Artifact Management"])
def copy_image(
    artifact: schemas.PostCopyImage
) -> schemas.PostCopyImageResponse:
    """
    API Endpoint to copy a Helm Chart/container image from one registry
    to another.
    """
    try:
        success = SkopeoClient.copy_image(
            src_registry=artifact.src_registry,
            src_image_name=artifact.src_image_name,
            src_image_tag=artifact.src_image_tag,
            dst_registry=artifact.dst_registry,
            dst_image_name=artifact.dst_image_name,
            dst_image_tag=artifact.dst_image_tag,
            src_username=artifact.src_username,
            src_password=artifact.src_password,
            dst_username=artifact.dst_username,
            dst_password=artifact.dst_password
        )
        return schemas.PostCopyImageResponse(success=success)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


# @app.post("/placeholder")
# def placeholder(
#     artifact: schemas.PostPlaceholder
# ) -> schemas.PostPlaceholderResponse:
#     raise HTTPException(status_code=501, detail="Not implemented")
