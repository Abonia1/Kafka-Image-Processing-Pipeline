import abc
import logging


class BaseService(abc.ABC):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    @abc.abstractmethod
    async def process(self, image_url: str, *args, **kwargs):
        """
        Abstract method to be implemented by subclasses.
        Each service will define how the image is processed.
        """
        pass
