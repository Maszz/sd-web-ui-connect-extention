from pydrive2.auth import GoogleAuth,AuthenticationRejected,AuthenticationError
from pydrive2.drive import GoogleDrive
from BaseConnector import BaseConnector
from PIL.Image import Image
from io import BytesIO
import base64
import json
import requests
import os
from modules import scripts
from PIL import PngImagePlugin
class GDriveConnector(BaseConnector):
    """
    Support only one folder
    """

    def __init__(self:str,client_secret_path:str, dir_name:str='sd_web_ui'):

        self.gauth = GoogleAuth('settings.yaml')
        self.gauth.DEFAULT_SETTINGS['client_config_backend'] = 'file'
        self.gauth.DEFAULT_SETTINGS['client_config_file'] = client_secret_path
        self.extension_path = os.path.dirname(os.path.realpath(__file__))
        try:
            self.gauth.LoadCredentialsFile(self.extension_path+"/credentials.json")
            if self.gauth.credentials is None:
                # Authenticate if they're not there
                self.gauth.LocalWebserverAuth()
            elif self.gauth.access_token_expired:
                # Refresh them if expired
                self.gauth.Refresh()
            else:
                # Initialize the saved creds
                self.gauth.Authorize()
            # Save the current credentials to a file
            self.gauth.SaveCredentialsFile(self.extension_path+"/credentials.json")
        except AuthenticationRejected :
            print("Authentication rejected")   
        except AuthenticationError:
            print("Authentication error")
       
        self.drive = GoogleDrive(self.gauth)
        self.dir_name = dir_name
        self.dir_id = self.get_gdrive_folder_id()

    def store_file(self, name:str, image:Image,png_info:dict):        
        if self.gauth.credentials.access_token is None:
            return
        with BytesIO() as output:
            pnginfo_data = PngImagePlugin.PngInfo()
            for k, v in png_info.items():
                pnginfo_data.add_text(k, str(v))
            image.save(output, format='png',quality=100,pnginfo=pnginfo_data)
            image_bytes = output.getvalue()
            self.save_image_request(image_bytes,name)
                

    def save_image_request(self,image_bytes:bytes,filename:str):
        """
        PyDrive seem to have issues with uploading bytes image, so we use api requests instead
        """
        metadata = {
            "name": filename.split('/')[-1] + '.png',
            "parents": [self.dir_id]
            }
        files = {
                'data': ('metadata', json.dumps(metadata), 'application/json'),
                'file': image_bytes
            }
        _ = requests.post(
            "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
            headers={"Authorization": "Bearer " + self.gauth.credentials.access_token},
            files=files
            )

    def get_gdrive_folder_id(self):
        folder_list = self.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        for folder in folder_list:
            if folder['title'] == self.dir_name:
                print("Folder found")
                return folder['id']
        print("Folder not found, creating new folder")
        self.create_folder()
        return None
    
    def create_folder(self):
        file_metadata = {
            'title': self.dir_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }

        folder = self.drive.CreateFile(file_metadata)
        folder.Upload()

    
    def before_unload(self):
        pass
        
    
