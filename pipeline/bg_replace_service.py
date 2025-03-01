from pipeline.base_service import BaseService
import fal_client
import logging


class BGReplaceService(BaseService):
    async def process(
        self, image_url: str, ref_image_url: str, prompt: str = "", *args, **kwargs
    ):
        model_name = "fal-ai/bria/background/replace"
        arguments = {
            "image_url": image_url,
            "ref_image_url": ref_image_url,
            "refine_prompt": True,
            "fast": True,
            "num_images": 1,
        }

        try:
            result = await fal_client.submit_async(model_name, arguments)
            async for event in result.iter_events(with_logs=True):
                logging.info(f"Event: {event}")

            final_result = await result.get()
            logging.info(f"BG replaced Processed Result: {final_result}")
            return final_result

        except fal_client.client.FalClientError as e:
            logging.error(f"FalClientError: {str(e)}")
        except Exception as e:
            logging.error(f"Unexpected Error: {str(e)}")

        return None
