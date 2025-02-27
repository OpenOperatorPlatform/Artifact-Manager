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
