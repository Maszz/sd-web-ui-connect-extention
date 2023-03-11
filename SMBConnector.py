import time
from functools import lru_cache
from io import BytesIO
from typing import Dict, List, Tuple

import numpy as np
from PIL import Image, PngImagePlugin
from smb.SMBConnection import SMBConnection

from BaseConnector import BaseConnector


class SMBConector(BaseConnector):

    """
    SMBConector: A class that implements Support Samba to store image files. amd manage the folder.

    Attributes
    ----------
    ip : str
        The ip address of the remote host.
    port : int
        The port number to connect to on the remote host.
    username : str
        The username to authenticate as (normally this is the user you log in as).
    password : str
        The password to use for authentication.
    service_name : str
        The service name to connect to on the remote host.
    server_name : str
        The server name to connect to on the remote host.(Should Match the netbios name in the smb.conf file),
        if not match it will be connection refused
    save_dir : str
        The directory name to save images in server.
    smb : SMBConnection
        The SMBConnection object.

    Methods
    -------
    store_file(name:str, image:Image, png_info:dict) -> None:
        try to upload image to remote host.
        via Samba protocol.
    before_unload() -> None:
        close the connection to the remote host.
    _dir_exist_or_create_dir() -> None:
        A private method that does not take in any parameters and does not return any value.

    """

    def __init__(
        self,
        username: str,
        password: str,
        local_name: str,
        server_name: str,
        service_name: str,
        domain: str,
        ip: str,
        port: int = 445,
        save_dir: str = "sd_web_ui",
    ) -> None:
        """
        initiate a SMBConector object. using SMBConnection. and create a folder in remote host if it doesn't exist.

        Parameters
        ----------
        username : str
            The username to authenticate as (normally this is the user you log in as).
        password : str
            The password to use for authentication.
        local_name : str
            The local name to connect to on the remote host.
        server_name : str
            The server name to connect to on the remote host.(Should Match the netbios name in the smb.conf file),
            if not match it will be connection refused
        service_name : str
            The service name to connect to on the remote host.
        domain : str
            The network domain. On windows, it is known as the workgroup.
        ip : str
            The ip address of the remote host.
        port : int
            The port number to connect to on the remote host.
        save_dir : str
            The directory name to save images in server.
        """
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.service_name = service_name
        self.server_name = server_name
        self.save_dir = save_dir
        self.smb = SMBConnection(
            username,
            password,
            local_name,
            server_name,
            domain=domain,
            use_ntlm_v2=True,
        )
        self.smb.connect(ip, port)
        self._dir_exist_or_create_dir()

    def store_file(self, name: str, image: Image.Image, png_info: dict) -> None:
        """
        Try to upload image to remote host.

        via Samba protocol.
        """
        with BytesIO() as output:
            pnginfo_data = PngImagePlugin.PngInfo()
            for k, v in png_info.items():
                pnginfo_data.add_text(k, str(v))
            image.save(output, format="png", quality=100, pnginfo=pnginfo_data)
            image_bytes = output.getvalue()
            name_splited = name.split("/")[-1]
            sub_dir = name.split("/")[1]
            print(f"Uploading {name_splited} to {self.save_dir}/{sub_dir}")
            self.smb.storeFile(
                self.service_name,
                f"{self.save_dir}/{sub_dir}/{name_splited}",
                BytesIO(image_bytes),
            )

    def before_unload(self) -> None:
        """Close the connection to the remote host."""
        self.smb.close()

    def _dir_exist_or_create_dir(self) -> None:
        """Create a folder in remote host if it doesn't exist."""
        for i in self.smb.listPath(self.service_name, "/"):
            if i.filename == self.save_dir:
                return
        self.smb.createDirectory(self.service_name, self.save_dir)
        self.smb.createDirectory(
            self.service_name, f"{self.save_dir}/txt2img-images")
        self.smb.createDirectory(
            self.service_name, f"{self.save_dir}/txt2img-grids")
        self.smb.createDirectory(
            self.service_name, f"{self.save_dir}/img2img-images")
        self.smb.createDirectory(
            self.service_name, f"{self.save_dir}/img2img-grids")
        self.smb.createDirectory(
            self.service_name, f"{self.save_dir}/extras-images")

    def traverse(self, sub_dir: str) -> List[str]:
        print(f"Listing {self.save_dir}/{sub_dir}")
        file_names = []
        for i in self.smb.listPath(self.service_name, f"{self.save_dir}/{sub_dir}"):
            file_names.append(f"{self.save_dir}/{sub_dir}/{i.filename}")
        print(f"Found {len(file_names)} files")
        # print(file_names)
        return file_names[2:]

    lru_cache(maxsize=512)

    def download(self, name: str) -> Tuple[np.ndarray, Dict[str, str]]:
        time.time()
        images = None
        info = None
        with BytesIO() as output:
            self.smb.retrieveFile(self.service_name, name, output)
            output.seek(0)
            temp = Image.open(output)
            info = temp.info
            images = np.array(temp)
        # print(f'Downloaded {name} in {time.time()-time1}')
        return images, info
