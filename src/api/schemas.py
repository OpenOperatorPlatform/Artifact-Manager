from pydantic import BaseModel, Field
from typing import Optional

class PostImageExists(BaseModel):
    registry_url: str = Field(default="registry.i2cat.net/adrian-private-project", description="Container registry URL including project")
    image_name: str = Field(default="nginx", description="Image name within the project")
    image_tag: str = Field(default="latest", description="Image tag to check")
    username: Optional[str] = Field(default=None, description="Optional username for authentication")
    password: Optional[str] = Field(default=None, description="Optional password for authentication")

class PostImageExistsResponse(BaseModel):
    exists: bool

class PostCopyImage(BaseModel):
    src_registry: str = Field(default="registry.i2cat.net/adrian-private-project", description="Source container registry URL including project")
    src_image_name: str = Field(default="nginx", description="Source image name")
    src_image_tag: str = Field(default="latest", description="Source image tag")

    dst_registry: str = Field(default="registry.i2cat.net/adrian-private-project-2", description="Destination container registry URL including project")
    dst_image_name: str = Field(default="nginx", description="Destination image name")
    dst_image_tag: str = Field(default="latest", description="Destination image tag")

    src_username: Optional[str] = Field(default=None, description="Optional username for source registry authentication")
    src_password: Optional[str] = Field(default=None, description="Optional password for source registry authentication")
    dst_username: Optional[str] = Field(default=None, description="Optional username for destination registry authentication")
    dst_password: Optional[str] = Field(default=None, description="Optional password for destination registry authentication")

class PostCopyImageResponse(BaseModel):
    success: bool
