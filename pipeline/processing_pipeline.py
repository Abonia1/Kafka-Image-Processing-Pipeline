import json
import logging
import datetime
import os
import shutil
import asyncio
from queue import Queue
from kafka import KafkaProducer
from pipeline.bg_removal_service import BGRemovalService
from pipeline.bg_replace_service import BGReplaceService
from pipeline.upscale_service import UpscaleService
import requests
from urllib.parse import urlparse
from utils.constants import BG_IMAGE


os.environ["FAL_KEY"] = "XXXXXXX"

logging.basicConfig(level=logging.INFO)


class ProcessingPipeline:
    def __init__(self, max_concurrent_requests=5):
        self.bg_removal_service = BGRemovalService()
        self.bg_replace_service = BGReplaceService()
        self.upscale_service = UpscaleService()
        self.max_concurrent_requests = max_concurrent_requests
        self.queue = Queue()
        # kafka_broker = os.getenv("KAFKA_BROKER", "localhost:9093")
        kafka_broker = "kafka:9093"
        self.kafka_producer = KafkaProducer(bootstrap_servers=kafka_broker)

    def start_processing(self, image_urls):
        # Produce Kafka message when processing starts
        self.kafka_producer.send(
            "image-processing-start",
            value=json.dumps({"status": "start", "images": image_urls}).encode(),
        )

        # Add the image URLs to the queue for processing
        for url in image_urls:
            self.queue.put(url)

        # Start processing in the background
        asyncio.create_task(self._process_images())

    async def _process_images(self):
        tasks = []
        while not self.queue.empty():
            image_url = self.queue.get()
            tasks.append(self._process_image(image_url))

            if len(tasks) >= self.max_concurrent_requests:
                # Wait for tasks concurrency limit
                await asyncio.gather(*tasks)
                tasks = []

        # Wait for remaining tasks to finish
        if tasks:
            await asyncio.gather(*tasks)

    async def get_valid_filename(self, url):
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)

        max_filename_length = 255
        if len(filename) > max_filename_length:
            filename = filename[:max_filename_length]

        return filename

    async def _process_image(self, image_url):
        logging.info(
            f"[START] Processing image {image_url} " f"at {datetime.datetime.now()}"
        )

        # Perform background removal
        bg_removed = await self.bg_removal_service.process(image_url)
        self.kafka_producer.send(
            "background-removal-start", value=json.dumps(bg_removed).encode()
        )

        bg_removed_url = bg_removed["image"]["url"]
        bg_removed_image = requests.get(bg_removed_url, stream=True)
        bg_removed_filename = await self.get_valid_filename(bg_removed_url)
        bg_removed_path = f"/app/static/{bg_removed_filename}"

        with open(bg_removed_path, "wb") as f:
            shutil.copyfileobj(bg_removed_image.raw, f)

        logging.info(f"Saved background removed image at {bg_removed_path}")
        bg_replaced = await self.bg_replace_service.process(
            bg_removed["image"]["url"],
            BG_IMAGE,
        )
        # bg_replaced = await self.bg_replace_service.process
        # (bg_removed['image']['url'], "/static/marble-bg.jpg")
        self.kafka_producer.send(
            "background-replacement-start", value=json.dumps(bg_replaced).encode()
        )

        # Save the background replaced image
        bg_replaced_url = bg_replaced["images"][0]["url"]
        bg_replaced_image = requests.get(bg_replaced_url, stream=True)
        bg_replaced_filename = await self.get_valid_filename(bg_replaced_url)
        bg_replaced_path = f"/app/static/{bg_replaced_filename}"

        with open(bg_replaced_path, "wb") as f:
            shutil.copyfileobj(bg_replaced_image.raw, f)
        logging.info(f"Saved background replaced image at {bg_replaced_path}")

        # Perform upscaling
        upscaled = await self.upscale_service.process(bg_replaced["images"][0]["url"])
        self.kafka_producer.send(
            "hyper-resolution-start", value=json.dumps(upscaled).encode()
        )

        # Save the upscaled image
        upscaled_url = upscaled["image"]["url"]
        upscaled_image = requests.get(upscaled_url, stream=True)
        upscaled_filename = await self.get_valid_filename(upscaled_url)
        upscaled_path = f"/app/static/{upscaled_filename}"

        with open(upscaled_path, "wb") as f:
            shutil.copyfileobj(upscaled_image.raw, f)
        logging.info(f"Saved upscaled image at {upscaled_path}")

        logging.info(
            f"[END] Finished processing image {image_url} at"
            f"{datetime.datetime.now()}"
        )
        self.kafka_producer.send(
            "image-processing-end",
            value=json.dumps(
                {"status": "end", "image_url": upscaled["image"]["url"]}
            ).encode(),
        )
