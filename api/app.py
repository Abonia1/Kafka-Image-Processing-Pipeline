from fastapi import FastAPI
from pydantic import BaseModel
from pipeline.processing_pipeline import ProcessingPipeline
from fastapi.staticfiles import StaticFiles
from typing import List


class ImageUrlsRequest(BaseModel):
    images: List[str]


app = FastAPI()

# Serve static files from the "static" directory
app.mount("/static", StaticFiles(directory="/app/static"), name="static")

pipeline = ProcessingPipeline()


@app.post("/process-images/")
async def process_images(request: ImageUrlsRequest):
    image_urls = request.images
    pipeline.start_processing(image_urls)
    return {
        "status": "processing started",
        "message": "Check Kafka for event streaming.",
    }
