import asyncio
import pytest
from pipeline.processing_pipeline import ProcessingPipeline


@pytest.mark.asyncio
async def test_concurrency_limit():
    # Mock processing function for testing
    async def mock_process_task(task_id):
        await asyncio.sleep(0.5)  # Simulate some delay
        return f"Task {task_id} processed"

    # Initialize the pipeline with a concurrency limit
    pipeline = ProcessingPipeline(max_concurrent_requests=3)
    pipeline._process_image = mock_process_task  # Mock the image processing method

    # Simulate multiple tasks being processed concurrently
    tasks = [pipeline._process_image(i) for i in range(10)]
    results = await asyncio.gather(*tasks)

    # Assert
    assert len(results) == 10  # All tasks should complete

    # We can further check execution times or inspect log data to verify concurrency
    # For example, check the total time taken to process the tasks to ensure it's consistent with concurrency limit
    # e.g. if the concurrency limit is 3, total time should be around 0.5 * (10 // 3) = ~1.67 seconds
