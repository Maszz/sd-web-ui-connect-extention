from typing import List,Type
from SMBConnector import SMBConector
from BaseConnector import BaseConnector
from PIL.Image import Image
from modules import shared
from typing import cast
from GDriveConnector import GDriveConnector
from SFTPConnector import SFTPConnector
class ConectorManager:

    def __init__(self):
        """
        This Class contains all the connector objects and is responsible for managing them.
        :warning: GDriveConnector is contained manual authentication flow with oauth provider 
        it need to seperate with other conectors and it will instantiate when app starts
        if you need to apply it you need to restart the webui server.
        
        """
        self.connector :List[BaseConnector] = list()
                
        
    def __reset__(self):
        self.connector = list()
    
    def create_smb_connector(self, username:str, password:str,local_name:str,server_name:str,service_name:str,domain:str,ip:str,port:int=445,save_dir:str='sd_web_ui'):
        smb_connector = SMBConector(username, password,local_name,server_name,service_name,domain,ip,port,save_dir)
        self.connector.append(smb_connector)

    
    def create_sftp_connector(self, host:str,username:str, password:str, remote_path='/',port=22):
        sftp_connector = SFTPConnector(host,username, password, remote_path,port)
        self.connector.append(sftp_connector)
    

    def create_gdrive_connector(self, client_secret:str ,save_dir:str='sd_web_ui',authen_only:bool=False):
        gdrive_connector = GDriveConnector(client_secret,save_dir)
        if authen_only:
            return
        self.connector.append(gdrive_connector)
    
    def create_dropbox_connector():
        raise NotImplementedError
    
    def save_image(self, image:Type[Image], name:str, png_info:dict):
        for connector in self.connector:
            connector.store_file(name, image, png_info)


    def before_unload(self):
        for connector in self.connector:
            connector.before_unload()