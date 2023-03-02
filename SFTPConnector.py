import paramiko
from BaseConnector import BaseConnector
from io import BytesIO
from PIL.Image import Image
from PIL import PngImagePlugin
class SFTPConnector(BaseConnector):
    def __init__(self, host:str, username:str, password:str ,remote_path:str='/' ,port:int=22):
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

        self.dir_exist_or_create_dir()
        # try:
        #     self.sftp.chdir(self.remote_path) 
        # except IOError:
        #     self.sftp.mkdir(self.remote_path) 
        #     self.sftp.chdir(self.remote_path)
   

    def store_file(self, name:str, image:Image, png_info:dict):
        
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

    def before_unload(self):
        self.sftp.close()
        self.ssh.close()

    def dir_exist_or_create_dir(self):
        try:
            self.sftp.chdir(self.remote_path) 
        except IOError:
            self.sftp.mkdir(self.remote_path)
            self.sftp.mkdir(f'{self.remote_path}/txt2img-images')
            self.sftp.mkdir(f'{self.remote_path}/txt2img-grids')
            self.sftp.mkdir(f'{self.remote_path}/img2img-images')
            self.sftp.mkdir(f'{self.remote_path}/img2img-grids')
            self.sftp.mkdir(f'{self.remote_path}/extras-images')
            self.sftp.chdir(self.remote_path)

