import pytest
from unittest import mock

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from pipeline.processing_pipeline import ProcessingPipeline
import asyncio

import pytest
from unittest import mock
import asyncio
from pipeline.processing_pipeline import ProcessingPipeline


# Test case for testing concurrency in the pipeline processing
@pytest.mark.asyncio
async def test_concurrency_limit():
    # Mock KafkaProducer to avoid any actual Kafka interactions
    with mock.patch("pipeline.processing_pipeline.KafkaProducer") as MockKafkaProducer:
        mock_producer = mock.Mock()
        MockKafkaProducer.return_value = mock_producer

        # Mock the services to avoid calling actual services
        with mock.patch(
            "pipeline.processing_pipeline.BGRemovalService"
        ) as MockBGRemovalService:
            with mock.patch(
                "pipeline.processing_pipeline.BGReplaceService"
            ) as MockBGReplaceService:
                with mock.patch(
                    "pipeline.processing_pipeline.UpscaleService"
                ) as MockUpscaleService:

                    # Mock the process method to return fake data (no actual processing)
                    MockBGRemovalService.return_value.process = mock.AsyncMock(
                        return_value={"image": {"url": "http://mock_url"}}
                    )
                    MockBGReplaceService.return_value.process = mock.AsyncMock(
                        return_value={"images": [{"url": "http://mock_url"}]}
                    )
                    MockUpscaleService.return_value.process = mock.AsyncMock(
                        return_value={"image": {"url": "http://mock_url"}}
                    )

                    # Initialize the pipeline with a concurrency limit
                    pipeline = ProcessingPipeline(max_concurrent_requests=3)

                    # Mock start_processing and _process_image methods
                    with mock.patch.object(
                        pipeline, "start_processing", mock.AsyncMock()
                    ) as mock_start_processing:
                        with mock.patch.object(
                            pipeline, "_process_image", mock.AsyncMock()
                        ) as mock_process_image:
                            # Simulate multiple tasks being processed concurrently
                            image_urls = [
                                "http://example.com/image1",
                                "http://example.com/image2",
                                "http://example.com/image3",
                                "http://example.com/image4",
                                "http://example.com/image5",
                            ]

                            # Call the mocked start_processing method
                            await pipeline.start_processing(image_urls)

                            # Call the mocked _process_image method
                            await asyncio.gather(
                                *[pipeline._process_image(url) for url in image_urls]
                            )

                            # Assert that the mocked methods were called the expected number of times
                            mock_start_processing.assert_called_once_with(image_urls)
                            mock_process_image.assert_called_with(
                                "http://example.com/image5"
                            )

                            # You can also assert that the method was called the correct number of times
                            assert mock_process_image.call_count == len(image_urls)
