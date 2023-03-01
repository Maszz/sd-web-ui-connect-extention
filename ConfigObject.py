from modules import shared
from typing import List,Type
class ConfigObject(object):
    """
    This class is used to store the configuration of the extensions
    """
    
    def get_smb_config(self):
        
        if(shared.opts.sd_web_ui_connect_smb_path == '' or shared.opts.sd_web_ui_connect_smb_user_passwd == '' or shared.opts.sd_web_ui_connect_smb_ip_port == '' or shared.opts.sd_web_ui_connect_smb_server_name_service_name == ''):
            return None

        smb_path_lst:List[str] = shared.opts.sd_web_ui_connect_smb_path.split(',')
        smb_domain_lst:List[str] = shared.opts.sd_web_ui_connect_smb_domain.split(',')
        smb_user_passwd_lst:List[str] = shared.opts.sd_web_ui_connect_smb_user_passwd.split(',')
        smb_ip_port_lst:List[str] = shared.opts.sd_web_ui_connect_smb_ip_port.split(',')
        smb_server_name_service_name_lst:List[str] = shared.opts.sd_web_ui_connect_smb_server_name_service_name.split(',')
        smb_user_passwd_lst_splited = [x.split(':') for x in smb_user_passwd_lst]
        smb_ip_port_lst_splited = [x.split(':') for x in smb_ip_port_lst]
        smb_server_name_service_name_lst_splited = [x.split(':') for x in smb_server_name_service_name_lst]

        preprocesed_setting = []

        if len(smb_path_lst) != len(smb_user_passwd_lst_splited) or len(smb_path_lst) != len(smb_ip_port_lst_splited) or len(smb_path_lst) != len(smb_server_name_service_name_lst_splited):
            return None

        for i in range(len(smb_path_lst)):
            smb_path = smb_path_lst[i]
            user = smb_user_passwd_lst_splited[i][0]
            passwd = smb_user_passwd_lst_splited[i][1]
            server_name = smb_server_name_service_name_lst_splited[i][0]
            service_name = smb_server_name_service_name_lst_splited[i][1]
            domain = smb_domain_lst[i]

            ip = smb_ip_port_lst_splited[i][0]
            port = smb_ip_port_lst_splited[i][1]
            temp = [user,passwd,"local",server_name,service_name,domain,ip,port,smb_path]
            preprocesed_setting.append(temp)
        return preprocesed_setting
    

    def get_gdrive_config(self):
        gdrive_client_secret = shared.opts.sd_web_ui_connect_gdrive_client_secret
        gdrive_save_dir = shared.opts.sd_web_ui_connect_gdrive_save_dir

        if  gdrive_client_secret == ''or gdrive_save_dir == '' :
            return None
        return ( gdrive_client_secret, gdrive_save_dir)
    
    def get_sftp_config(self):
      
        if (shared.opts.sd_web_ui_connect_sftp_user_passwd == '' or shared.opts.sd_web_ui_connect_sftp_ip_port == ''):
            return None
        
        sftp_user_passwd_lst:List[str] = shared.opts.sd_web_ui_connect_sftp_user_passwd.split(',')
        sftp_ip_port_lst:List[str] = shared.opts.sd_web_ui_connect_sftp_ip_port.split(',')
        sftp_user_passwd_lst_splited = [x.split(':') for x in sftp_user_passwd_lst]
        sftp_ip_port_lst_splited = [x.split(':') for x in sftp_ip_port_lst]
        sftp_remote_path:List[str] = shared.opts.sd_web_ui_connect_sftp_remote_path.split(',')
        preprocesed_setting = []

        if len(sftp_ip_port_lst_splited) ==0 or len(sftp_user_passwd_lst_splited) == 0:
            return None

        if len(sftp_ip_port_lst_splited) != len(sftp_user_passwd_lst_splited):
            return None
        
        for i in range(len(sftp_user_passwd_lst)):
            user = sftp_user_passwd_lst_splited[i][0]
            passwd = sftp_user_passwd_lst_splited[i][1]
            ip = sftp_ip_port_lst_splited[i][0]
            port = sftp_ip_port_lst_splited[i][1]
            temp = [ip,user,passwd,sftp_remote_path[i],port]
            preprocesed_setting.append(temp)

        return preprocesed_setting