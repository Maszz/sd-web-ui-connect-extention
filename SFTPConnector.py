from io import BytesIO

import paramiko
from PIL import PngImagePlugin
from PIL.Image import Image

from BaseConnector import BaseConnector


class SFTPConnector(BaseConnector):

    """
    SFTPConnector: A class that implements Support file transfer protocol (SFTP) to store image files.

    Attributes
    ----------
    host : str
        The host name or IP address of the remote host.
    username : str
        The username to authenticate as (normally this is the user you log in as).
    password : str
        The password to use for authentication.
    port : int
        The port number to connect to on the remote host.
    remote_path : str
        The remote path to store the image file.
    ssh : paramiko.SSHClient
        The SSHClient object.
    sftp : paramiko.SFTPClient
        The SFTPClient object.

    Methods
    -------
    store_file(name:str, image:Image, png_info:dict) -> None:
        try to upload image to remote host.
        via SFTP protocol.

    before_unload() -> None:
        close the connection to the remote host.

    _dir_exist_or_create_dir() -> None:
        A private method that does not take in any parameters and does not return any value.
        This method is invoked when the SFTPConnector object is instantiated.
        This method checks if the remote path exists, if not, it creates the remote path.
    """

    def __init__(self, host:str, username:str, password:str ,remote_path:str='/' ,port:int=22) -> None:
        """
        initiate a SFTPConnector object. using paramiko. and create a folder in remote host if it doesn't exist.

        Parameters
        ----------
        host : str
            The host name or IP address of the remote host.
        username : str
            The username to authenticate as (normally this is the user you log in as).
        password : str
            The password to use for authentication.
        port : int
            The port number to connect to on the remote host.
        remote_path : str
            The remote path to store the image file.
        """
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.remote_path = remote_path
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print(host, username, password, remote_path, port)
        self.ssh.connect(self.host, self.port, self.username, self.password)
        self.sftp = self.ssh.open_sftp()
        self._dir_exist_or_create_dir()

    def store_file(self, name:str, image:Image, png_info:dict)->None:
        """Performs store the image file with the given name and png_info via sftp."""
        with BytesIO() as output:
            pnginfo_data = PngImagePlugin.PngInfo()
            for k, v in png_info.items():
                pnginfo_data.add_text(k, str(v))
            image.save(output, format='png',quality=100,pnginfo=pnginfo_data)
            image_bytes = output.getvalue()
            name_splited = name.split('/')[-1]
            sub_dir = name.split('/')[1]
            print(f'Uploading {name_splited} to {self.remote_path}/{sub_dir}')

            self.sftp.putfo(BytesIO(image_bytes), f'{sub_dir}/{name_splited}')

    def before_unload(self)->None:
        """Performs close the connection to the remote host."""
        self.sftp.close()
        self.ssh.close()

    def _dir_exist_or_create_dir(self)->None:
        try:
            self.sftp.chdir(self.remote_path)
        except OSError:
            self.sftp.mkdir(self.remote_path)
            self.sftp.mkdir(f'{self.remote_path}/txt2img-images')
            self.sftp.mkdir(f'{self.remote_path}/txt2img-grids')
            self.sftp.mkdir(f'{self.remote_path}/img2img-images')
            self.sftp.mkdir(f'{self.remote_path}/img2img-grids')
            self.sftp.mkdir(f'{self.remote_path}/extras-images')
            self.sftp.chdir(self.remote_path)

