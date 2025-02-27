from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from . import schemas
from src.skopeo.skopeo import SkopeoClient

app = FastAPI()

@app.get("/", include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse(url="/docs")

@app.post("/image-exists")
def image_exists(artifact: schemas.PostImageExists) -> schemas.PostImageExistsResponse:
    """
    API endpoint to check if an image with a specific tag exists in a repository.
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

# @app.post("/placeholder")
# def placeholder(artifact: schemas.PostPlaceholder) -> schemas.PostPlaceholderResponse:
#     raise HTTPException(status_code=501, detail="Not implemented")
