from pydantic import BaseModel
from typing import List, Optional

class PostImageExists(BaseModel):
    registry_url: str
    repository: str
    image_tag: str
    username: Optional[str] = None
    password: Optional[str] = None

class PostImageExistsResponse(BaseModel):
    exists: bool
