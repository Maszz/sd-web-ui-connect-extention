from typing import List, Type

from PIL.Image import Image

from BaseConnector import BaseConnector
from GDriveConnector import GDriveConnector
from SFTPConnector import SFTPConnector
from SMBConnector import SMBConector


class ConnectorManager:

    """
    ConnectorManager: A class that manages all the connector objects.

    It is responsible for creating and storing the connector objects and invoking a Connector method.

    Attributes
    ----------
    connector : List[BaseConnector]
        A list of connector objects.

    Methods
    -------
    create_smb_connector(username:str, password:str,local_name:str,server_name:str,service_name:str,domain:str,ip:str,port:int=445,save_dir:str='sd_web_ui') -> None:
        Create a SMBConnector object and add it to the connector list.
    create_sftp_connector(host:str,username:str, password:str, remote_path='/',port=22) -> None:
        Create a SFTPConnector object and add it to the connector list.
    """

    def __init__(self) -> None:
        """
        Initiate a empty connector list.

        :warning: GDriveConnector is contained manual authentication flow with oauth provider(Deprecated).
        it need to seperate with other conectors and it will instantiate when app starts
        if you need to apply it you need to restart the webui server.
        """
        self.connector: List[BaseConnector] = []

    def __reset__(self) -> None:
        """Reset the connector list.This will get Invoke when want to reset an attribute."""
        self.connector = []

    def create_smb_connector(
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
        """Wrapper around SMBConnector class. for creating a SMBConnector object and add it to the connector list."""
        smb_connector = SMBConector(
            username,
            password,
            local_name,
            server_name,
            service_name,
            domain,
            ip,
            port,
            save_dir,
        )
        self.connector.append(smb_connector)

    def create_sftp_connector(
        self,
        host: str,
        username: str,
        password: str,
        remote_path: str = "/",
        port: int = 22,
    ) -> None:
        """Wrapper around SFTPConnector class. for creating a SFTPConnector object and add it to the connector list."""
        sftp_connector = SFTPConnector(
            host, username, password, remote_path, port)
        self.connector.append(sftp_connector)

    def create_gdrive_connector(
        self,
        client_secret: str,
        save_dir: str = "sd_web_ui",
        authen_only: bool = False,
    ) -> None:
        """
        Wrapper around GDriveConnector class. for creating a GDriveConnector object and add it to the connector list.

        When Only initiate for authentication only is use for the first time. for geting the access token.
        """
        gdrive_connector = GDriveConnector(client_secret, save_dir)
        if authen_only:
            return
        self.connector.append(gdrive_connector)

    def create_dropbox_connector() -> None:
        """Wrapper around DropboxConnector class. for creating a DropboxConnector object and add it to the connector list."""
        raise NotImplementedError

    def save_image(self, image: Type[Image], name: str, png_info: dict) -> None:
        """Invoke the store_file method of all the connector objects."""
        for connector in self.connector:
            connector.store_file(name, image, png_info)

    def _ui_get_smb_connector(
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
    ) -> SMBConector:
        smb = SMBConector(
            username,
            password,
            local_name,
            server_name,
            service_name,
            domain,
            ip,
            port,
            save_dir,
        )
        return smb

    def _ui_get_sftp_connector(
        self,
        host: str,
        username: str,
        password: str,
        remote_path: str = "/",
        port: int = 22,
    ) -> SFTPConnector:
        sftp = SFTPConnector(host, username, password, remote_path, port)
        return sftp

    def before_unload(self) -> None:
        """Invoke the before_unload method of all the connector objects."""
        for connector in self.connector:
            connector.before_unload()
