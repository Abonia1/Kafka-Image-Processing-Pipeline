import asyncio
import logging
import os
from pipeline.bg_removal_service import BGRemovalService
from pipeline.bg_replace_service import BGReplaceService
from pipeline.upscale_service import UpscaleService

os.environ["FAL_KEY"] = "XXXXXXX"

# Configure logging
logging.basicConfig(level=logging.INFO)


async def test_bg_removal(image_url):
    service = BGRemovalService()
    logging.info(f"Testing Background Removal for image URL: {image_url}")

    result = await service.process(image_url)

    if result:
        logging.info(f"Background Removal Result: {result}")
    else:
        logging.error("Background Removal failed")


async def test_bg_replace(image_url, ref_image_url):
    service = BGReplaceService()
    logging.info(
        f"Testing Background Replacement for image URL: {image_url} using reference image URL: {ref_image_url}"
    )

    result = await service.process(image_url, ref_image_url)

    if result:
        logging.info(f"Background Replacement Result: {result}")
    else:
        logging.error("Background Replacement failed")


async def test_upscale(image_url):
    service = UpscaleService()
    logging.info(f"Testing Image Upscaling for image URL: {image_url}")

    result = await service.process(image_url, scale=2.0, model="RealESRGAN_x4plus")

    if result:
        logging.info(f"Upscaling Result: {result}")
    else:
        logging.error("Upscaling failed")


async def main():
    # Example URLs for testing
    image_url = "https://storage.googleapis.com/falserverless/model_tests/remove_background/elephant.jpg"
    ref_image_url = (
        "https://storage.googleapis.com/falserverless/bria/bria_bg_replace_bg.jpg"
    )
    # ref_image_url="static/marble-bg.jpg"

    # Run all the tests
    await asyncio.gather(
        # test_bg_removal(image_url),
        # test_bg_replace(image_url, ref_image_url),
        test_upscale(image_url),
    )


if __name__ == "__main__":
    asyncio.run(main())
