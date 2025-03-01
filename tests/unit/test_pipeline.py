import sys
import os
import pytest
import asyncio
from unittest.mock import MagicMock
from pipeline.processing_pipeline import ProcessingPipeline

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))


@pytest.fixture
def mock_services():
    bg_removal_mock = MagicMock()
    bg_replace_mock = MagicMock()
    upscale_mock = MagicMock()

    # Mock the service responses
    bg_removal_mock.process.return_value = {
        "image": {"url": "https://example.com/bg_removed.jpg"}
    }
    bg_replace_mock.process.return_value = {
        "images": [{"url": "https://example.com/bg_replaced.jpg"}]
    }
    upscale_mock.process.return_value = {
        "image": {"url": "https://example.com/upscaled.jpg"}
    }

    pipeline = ProcessingPipeline(max_concurrent_requests=5)
    pipeline.bg_removal_service = bg_removal_mock
    pipeline.bg_replace_service = bg_replace_mock
    pipeline.upscale_service = upscale_mock

    return pipeline


def test_concurrency_limit(mock_services):
    image_urls = [
        "https://example.com/image1.jpg"
    ] * 10  # 10 images, concurrency limit is 5
    mock_services.start_processing(image_urls)

    # Wait for async tasks to complete
    asyncio.run(mock_services._process_images())

    # Ensure no more than 5 concurrent tasks are running
    assert mock_services.bg_removal_service.process.call_count <= 5
    assert mock_services.bg_replace_service.process.call_count <= 5
    assert mock_services.upscale_service.process.call_count <= 5


def test_kafka_event_flow(mock_services):
    image_urls = ["https://example.com/image1.jpg"]
    mock_services.start_processing(image_urls)

    # Ensure Kafka producer sends the correct messages
    mock_services.kafka_producer.send.assert_any_call(
        "image-processing-start",
        value='{"status": "start", "images": ["https://example.com/image1.jpg"]}'.encode(),
    )
    mock_services.kafka_producer.send.assert_any_call(
        "image-processing-end",
        value='{"status": "end", "image_url": "https://example.com/upscaled.jpg"}'.encode(),
    )
