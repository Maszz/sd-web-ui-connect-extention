"""
Contain the root of the extension that will get called by the webui.

This file is the entry point of the extension. It will be called by the webui when the extension is loaded.
This file seperated into 2 parts:
    1. Initiate the extension.
    2. helper methods for setting up the extension.
    3. register the callbacks hook.
"""
import warnings
from typing import Type, cast

from fastapi import FastAPI
from gradio import Blocks
from modules import script_callbacks, shared
from modules.script_callbacks import ImageSaveParams
from PIL.Image import Image

from ConfigObject import ConfigObject
from ConnectorManager import ConnectorManager
from UI import UI

warnings.warn("CryptographyDeprecationWarning", DeprecationWarning)

def setup_options()->None:
    """For multiple connections use , to separate them."""
    shared.options_templates.update(shared.options_section(('sd_web_ui_connect', "Remote Drive"), {
    "sd_web_ui_connect_smb_path":shared.OptionInfo("", "Output directory for images; if empty, it will be sd_web_ui", component_args=shared.hide_dirs),
    "sd_web_ui_connect_smb_user_passwd":shared.OptionInfo("", "Username/Password for smb server connect(must be in this format 'username:password' and use comma(,) for seperate them when have multiple connections) E.g user1:pass1,user2:pass2", component_args=shared.hide_dirs),
    "sd_web_ui_connect_smb_ip_port":shared.OptionInfo("", "Ip/port for connect to smb server(must be in this format 'ip:port' and use comma(,) for seperate them when have multiple connections) E.g ip1:port1,ip2:port2", component_args=shared.hide_dirs),
    "sd_web_ui_connect_smb_server_name_service_name":shared.OptionInfo("", "remote name/service_name of smb server(must be in this format 'remote_name:service_name' and use comma(,) for seperate them when have multiple connections) E.g remote_name1:service_name1,remote_name2:service_name2", component_args=shared.hide_dirs),
    "sd_web_ui_connect_smb_domain":shared.OptionInfo("", "domain(WORKGROUP) of smb server", component_args=shared.hide_dirs),
    "sd_web_ui_connect_delete_on_remote_save": shared.OptionInfo(False, "Delete image from save directory when successful save image on remote drive"),
    "sd_web_ui_connect_gdrive_client_secret":shared.OptionInfo("", "google oauth path to client_secret **Need absolute path(After Apply gdrive config app if use have another gdrive oauth apply before you need to delete credentails.json in extension folder)", component_args=shared.hide_dirs),
    "sd_web_ui_connect_gdrive_save_dir":shared.OptionInfo("", "save dir (After Apply gdrive config app ui need to restart)", component_args=shared.hide_dirs),
    "sd_web_ui_connect_sftp_user_passwd":shared.OptionInfo("", "Username/Password for sftp server connect(must be in this format 'username:password' and use comma(,) for seperate them when have multiple connections) E.g user1:pass1,user2:pass2", component_args=shared.hide_dirs),
    "sd_web_ui_connect_sftp_ip_port":shared.OptionInfo("", "Ip/port for connect to sftp server(must be in this format 'ip:port' and use comma(,) for seperate them when have multiple connections) E.g ip1:port1,ip2:port2", component_args=shared.hide_dirs),
    "sd_web_ui_connect_sftp_remote_path":shared.OptionInfo("", "Path to connection to sftp server (path contain trailing slash E.g /NasStorage/sd_web_ui)", component_args=shared.hide_dirs),


}))

def on_app_started(gradio:Blocks,fastapi:FastAPI)->None:
    """Need to authen first when app started for get access token."""
    setting_lst_gdrive = config.get_gdrive_config()
    if setting_lst_gdrive is not None:
        manager.create_gdrive_connector(setting_lst_gdrive[0],setting_lst_gdrive[1],authen_only=True)

    pass


def save_image_callback(params: ImageSaveParams)->None:
    """Logic to perfrom save image for this extension, that will be registered to the webui."""
    manager.__reset__()
    setup_connectors(manager,config)
    image = cast(Type[Image],params.image)  # ImageSaveParams not provide type to its this made for support type hinting
    image_name = params.filename
    manager.save_image(image,image_name,params.pnginfo)
    manager.before_unload()


def setup_connectors(manager:ConnectorManager,config:ConfigObject)->None:
    """Setup all connectors that will be used by this extension, helper method for `save_image_callback`."""
    setting_lst = config.get_smb_config()
    if(setting_lst is not None):
        for setting in setting_lst:
            manager.create_smb_connector(setting[0],setting[1],setting[2],setting[3],setting[4],setting[5],setting[6],setting[7],setting[8])

    setting_lst_sftp = config.get_sftp_config()
    if setting_lst_sftp is not None:
        for setting in setting_lst_sftp:
            manager.create_sftp_connector(setting[0],setting[1],setting[2],setting[3],setting[4])
    setting_lst_gdrive = config.get_gdrive_config()
    if setting_lst_gdrive is not None:
        manager.create_gdrive_connector(setting_lst_gdrive[0],setting_lst_gdrive[1])

manager = ConnectorManager()
config = ConfigObject()
ui = UI(manager)


script_callbacks.on_ui_settings(setup_options)
script_callbacks.on_app_started(on_app_started)
script_callbacks.on_before_image_saved(save_image_callback)
script_callbacks.on_ui_tabs(ui.on_ui_tabs)

