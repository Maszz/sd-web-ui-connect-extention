import json
import os
from io import BytesIO

import requests
from PIL import PngImagePlugin
from PIL.Image import Image
from pydrive2.auth import AuthenticationError, AuthenticationRejected, GoogleAuth
from pydrive2.drive import GoogleDrive

from BaseConnector import BaseConnector


class GDriveConnector(BaseConnector):

    """
    GDriveConnector: A class that implements Support Google Drive to store image files and manage the folder.

    Attributes
    ----------
    gauth : GoogleAuth
        The GoogleAuth object.
    extension_path : str
        The path to the extension folder.
    drive : GoogleDrive
        The GoogleDrive object.
    dir_name : str
        The name of the folder in google drive.
    dir_id : str
        The id of the folder in google drive.

    Methods
    -------
    store_file(name:str, image:Image, png_info:dict) -> None:
        try to upload image to google drive.

    _save_image_request(image_bytes:bytes, filename:str) -> None:
        Performs http request to google drive api for upload image.
    """

    def __init__(self,client_secret_path:str, dir_name:str='sd_web_ui') -> None:
        """
        Initiate a GDriveConnector object. using pydrive2. and create a folder in google drive if it doesn't exist.

        Parameters
        ----------
        client_secret_path : str
            The path to the client_secret.json file.
        dir_name : str
            The name of the folder in google drive.
        """
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

    def store_file(self, name:str, image:Image,png_info:dict)->None:
        """Upload a file to google drive."""
        if self.gauth.credentials.access_token is None:
            return
        with BytesIO() as output:
            pnginfo_data = PngImagePlugin.PngInfo()
            for k, v in png_info.items():
                pnginfo_data.add_text(k, str(v))
            image.save(output, format='png',quality=100,pnginfo=pnginfo_data)
            image_bytes = output.getvalue()
            self._save_image_request(image_bytes,name)


    def _save_image_request(self,image_bytes:bytes,filename:str)->None:
        """
        sent api request to google drive api fir upload image.

        PyDrive seem to have issues with uploading bytes image, so we use api requests instead.
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

    def get_gdrive_folder_id(self)->None:
        """Get the folder id of the folder in google drive."""
        folder_list = self.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        for folder in folder_list:
            if folder['title'] == self.dir_name:
                print("Folder found")
                return folder['id']
        print("Folder not found, creating new folder")
        self.create_folder()
        return None

    def create_folder(self)->None:
        """Create a folder in google drive."""
        file_metadata = {
            'title': self.dir_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }

        folder = self.drive.CreateFile(file_metadata)
        folder.Upload()


    def before_unload(self)->None:
        pass


