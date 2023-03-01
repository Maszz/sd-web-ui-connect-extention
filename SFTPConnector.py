import paramiko
from BaseConnector import BaseConnector
from io import BytesIO
from PIL.Image import Image
class SFTPConnector(BaseConnector):
    def __init__(self, host:str, username:str, password:str ,remote_path:str='/' ,port:int=22):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.remote_path = remote_path
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        self.ssh.connect(self.host, self.port, self.username, self.password)
        self.sftp = self.ssh.open_sftp()

        try:
            self.sftp.chdir(self.remote_path) 
        except IOError:
            self.sftp.mkdir(self.remote_path) 
            self.sftp.chdir(self.remote_path)
   

    def store_file(self, name:str, image:Image):
        
        with BytesIO() as output:
            image.save(output, format='png')
            image_bytes = output.getvalue()
            name_splited = name.split('/')[-1]
            print(f'Uploading {name_splited} to {self.remote_path}')

            self.sftp.putfo(BytesIO(image_bytes), f'{name_splited}')

    def before_unload(self):
        self.sftp.close()
        self.ssh.close()

