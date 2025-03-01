from pydantic import BaseModel
from typing import List


class ImageProcessingRequest(BaseModel):
    images: List[str]


class ImageProcessingResponse(BaseModel):
    status: str
    message: str = None
    details: dict = None
