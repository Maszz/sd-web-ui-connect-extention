import abc
from typing import Dict, List, Tuple, Type

from numpy import ndarray
from PIL.Image import Image


class BaseConnector(metaclass=abc.ABCMeta):

    """
    BaseConnector: An abstract base class that defines two abstract methods that must be implemented by all connector.

    Methods
    -------
    store_file(name:str, image:Type[Image],png_info:dict) -> None:
        An abstract method that takes in a string name,
        an instance of the Image class, and a dictionary png_info and does not return any value.
        This method should implement the logic for storing the image file with the given name and png_info.
        This method is invoked when  extension get image from webui lifecycle hooks.

    before_unload() -> None:
        An abstract method that does not take in any parameters and does not return any value.
        This methods is invoked after image is saved.
    """

    @abc.abstractmethod
    def store_file(self, name: str, image: Type[Image], png_info: dict) -> None:
        """
        Perform saving the image file with the given name and png_info to the file system.

        Parameters
        ----------
        name : str
            raw path of the original image file.

        image : Type[Image]
            An instance of the PIL Image class.

        png_info : dict[str, str]
            A dictionary containing the png_info of the image file.
            Should be a file meta data.
        """
        pass

    @abc.abstractmethod
    def before_unload(self) -> None:
        """Perform a cleaning function for this connector."""
        pass

    @abc.abstractmethod
    def traverse(self, sub_dir: str) -> List[str]:
        """
        List all files in a directory.

        Parameters
        ----------
        sub_dir : str
            The sub directory to list files in.
        """
        pass

    @abc.abstractmethod
    def download(self, name: str) -> Tuple[ndarray, Dict[str, str]]:
        """
        Download a file from remote host.

        Parameters
        ----------
        name : str
            The name of the file to download(Path).

        Returns
        -------
        Tuple[ndarray,Dict[str,str]]
            A tuple containing the image data and the png_info of the image file.
        """
        pass
