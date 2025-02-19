from pydantic import BaseModel

class PostCopyArtifact(BaseModel):
    src_url: str
    src_image_name: str
    src_image_tag: str
    dst_url: str
    dst_image_name: str
    dst_image_tag: str

class PostCopyArtifactResponse(BaseModel):
    message: str
