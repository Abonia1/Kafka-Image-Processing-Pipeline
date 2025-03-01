from pipeline.base_service import BaseService
import fal_client
import logging


class BGRemovalService(BaseService):
    async def process(self, image_url: str, *args, **kwargs):
        model_name = "fal-ai/imageutils/rembg"
        arguments = {"image_url": image_url}

        try:
            result = await fal_client.submit_async(model_name, arguments)
            async for event in result.iter_events(with_logs=True):
                logging.info(f"Event: {event}")

            final_result = await result.get()
            logging.info(f"Processed Result: {final_result}")
            return final_result

        except fal_client.client.FalClientError as e:
            logging.error(f"FalClientError: {str(e)}")
        except Exception as e:
            logging.error(f"Unexpected Error: {str(e)}")

        return None
