from fastapi import FastAPI, HTTPException
# from src.skopeo import client # Placeholder
from . import schemas

app = FastAPI()

@app.get("/")
def hello_world():    
    return {"message": "Hello World"}

@app.post("/copy")
def copy_artefact(copy_info: schemas.PostCopyArtifact) -> schemas.PostCopyArtifactResponse:
    # return {"message": "Artifact {}:{} from node {} copied to node {}".format(copy_info.src_image_name, copy_info.src_image_tag, copy_info.src_url, copy_info.dst_url)}
    # skopeo_response = client.copy_artifact_from(src_url, dst_url)
    return schemas.PostCopyArtifactResponse(message="Artifact {}:{} from node {} copied to node {}".format(copy_info.src_image_name, copy_info.src_image_tag, copy_info.src_url, copy_info.dst_url))

# @app.post("/copy_test")
# def copy_artefact(copy_info: schemas.PostCopyArtifact) -> schemas.PostCopyArtifactResponse:
#     raise HTTPException(status_code=501, detail="Not implemented")
