from smb.SMBConnection import SMBConnection
from io import BytesIO 
from BaseConnector import BaseConnector
from PIL.Image import Image
from uuid import UUID

class SMBConector(BaseConnector):

    def __init__(self, username:str, password:str,local_name:str,server_name:str,service_name:str,domain:str,ip:str,port:int=445,save_dir:str='sd_web_ui'):
        """
        :param string ip: IP address
        :param int port: Port
        :param string username: Username
        :param string password: Password
        :param string local_name: Local Machine name(anything you want).
        :param string server_name: Server name (Should Match the netbios name in the smb.conf file), 
            if not match it will be connection refused
        :param string service_name: Service name (Should Match the workgroup),
        :param string domain: in Window in call workGroup (Should Match the workgroup in the smb.conf file),
        :param string save_dir: directory name to save images in server
        """
        

        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.service_name = service_name
        self.server_name = server_name
        self.save_dir = save_dir
        self.smb = SMBConnection(username, password,local_name,server_name, domain=domain, use_ntlm_v2 = True)
        self.smb.connect(ip, port)
        self.dir_exist_or_create_dir()
      

    def store_file(self, name:str, image:Image):
        with BytesIO() as output:
            image.save(output, format='png')
            image_bytes = output.getvalue()
            name_splited = name.split('/')[-1]
            print(f'Uploading {name_splited} to {self.save_dir}')
            self.smb.storeFile(self.service_name,f'{self.save_dir}/{name_splited}',BytesIO(image_bytes))

    def before_unload(self):
        self.smb.close()
    
    def dir_exist_or_create_dir(self):
        for i in self.smb.listPath(self.service_name,'/'):
            if i.filename == self.save_dir:
                return 
        self.smb.createDirectory(self.service_name,self.save_dir) 

    