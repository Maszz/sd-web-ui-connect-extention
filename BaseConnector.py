import abc
from PIL.Image import Image
from typing import Type

class BaseConnector(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def store_file(self, name:str, image:Type[Image]):
        pass

    @abc.abstractmethod
    def before_unload(self):
        pass