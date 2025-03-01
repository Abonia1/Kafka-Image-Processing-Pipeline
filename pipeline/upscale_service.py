from pipeline.base_service import BaseService
import fal_client
import logging


class UpscaleService(BaseService):
    async def process(
        self,
        image_url: str,
        scale: float = 2.0,
        model: str = "RealESRGAN_x4plus",
        *args,
        **kwargs,
    ):
        model_name = "fal-ai/esrgan"
        arguments = {
            "image_url": image_url,
            "scale": scale,
            "model": model,
            "output_format": "png",
        }
        try:
            result = await fal_client.submit_async(model_name, arguments)
            async for event in result.iter_events(with_logs=True):
                logging.info(f"Event: {event}")

            final_result = await result.get()
            logging.info(f"Upscaling Processed Result: {final_result}")
            return final_result

        except fal_client.client.FalClientError as e:
            logging.error(f"FalClientError: {str(e)}")
        except Exception as e:
            logging.error(f"Unexpected Error: {str(e)}")

        return None
