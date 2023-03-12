import time as time_lib
from typing import Any, Dict, List, Tuple, Union

import gradio as gr
import numpy as np
from modules.shared import opts

from ConfigObject import ConfigObject
from ConnectorManager import ConnectorManager


class UI:

    """
    UI class is used to create the UI of the remote image webui.

    This class contains gradio ui elements and functions that are used to create the UI of the remote image webui.
    and also contains functions to manage the ui elements.

    Attributes
    ----------
    manager : ConnectorManager
        The connector manager object that is used to manage the connectors.
    tab_lst : List[str]
        A list of the tabs that are used in the UI.
    num_images_per_page : int
        The number of images that are displayed per page.
    image_ext_list : List[str]
        A list of the image extensions that are supported.
    config : ConfigObject
        The config object that is used to get the config data.
    selected_type : str
        The selected connector type.
    selected_index : int
        The selected connector index.
    img_lst : List[str]
        A list of the images that are displayed in the UI.
    """

    def __init__(self, manager: ConnectorManager) -> None:
        """
        Initiate the UI object.

        :param manager: The connector manager object that is used to manage the connectors.
        """
        self.manager = manager
        self.tab_lst = [
            "txt2img",
            "img2img",
            "txt2img-grids",
            "img2img-grids",
            "Extras",
        ]
        self.num_images_per_page = 60
        self.image_ext_list = [
            ".png",
            ".jpg",
            ".jpeg",
            ".bmp",
            ".gif",
            ".webp",
        ]
        self.config = ConfigObject()
        self.selected_type = "SMB"
        self.selected_index = 0
        self.connector = None
        self.connection_type = "SMB"
        self.get_connetor("SMB", 1)
        self.img_lst = []

    def get_connetor(self, v: str, s: int) -> int:
        """
        Perform the connection to the remote host to selected connector.

        Parameters
        ----------
        v : str
            The connector type.
        s : int
            state for trigger gradio update.
        """
        print("get_connetor")
        if v == "SMB":
            config = self.config.get_smb_config()
            selected_config = config[self.selected_index]
            self.connector = self.manager._ui_get_smb_connector(
                selected_config[0],
                selected_config[1],
                selected_config[2],
                selected_config[3],
                selected_config[4],
                selected_config[5],
                selected_config[6],
                selected_config[7],
                selected_config[8],
            )
        elif v == "SFTP":
            config = self.config.get_sftp_config()
            selected_config = config[self.selected_index]
            self.connector = self.manager._ui_get_sftp_connector(
                selected_config[0],
                selected_config[1],
                selected_config[2],
                selected_config[3],
                selected_config[4],
            )
        else:
            self.connector = None

        return -s

    def get_connector_no(self, connector_type: str) -> Union[Dict[str, Any], None]:
        """
        Update the gradio radio element with the size of config.

        Parameters
        ----------
        connector_type : str
            The connector type.
        """
        if connector_type == "SMB":
            config = self.config.get_smb_config()
            return gr.Radio.update(choices=[str(i) for i in range(len(config))])

        if connector_type == "SFTP":
            config = self.config.get_sftp_config()
            if config is None:
                self.connector = None
                return gr.Radio.update(choices=[])
            return gr.Radio.update(choices=[str(i) for i in range(len(config))])

    def change_connector(self, connector_no: int, renew: int) -> int:
        """Change the connector(Get from gradio radio)."""
        self.selected_index = connector_no
        return -renew

    def on_ui_tabs(self) -> Tuple[gr.Blocks, str, str]:
        """
        Return the UI tabs. of gradio elements w/ tab names and tab ids.

        This method use for register `on_ui_tabs` callback function on webui.
        """
        with gr.Blocks(analytics_enabled=False) as images_browser:
            with gr.Tabs(elem_id="connect_browser_tab"):
                for tab in self.tab_lst:
                    with gr.Tab(tab):
                        with gr.Blocks(analytics_enabled=False):
                            self.create_tab(tab)
            gr.Textbox(
                ",".join(self.tab_lst),
                elem_id="connect_browser_tabnames_list",
                visible=False,
            )

        return ((images_browser, "Connect Image Browser", "connect_image_browser"),)

    def create_tab(self, tab: str) -> None:
        """
        Create specific tab elements of remote browser.

        This methods contains all of statements that are used to create the UI elements of the remote browser webui.
        """
        dir_name = ""
        if tab == "txt2img":
            dir_name = opts.outdir_txt2img_samples.split("/")[-1]
        elif tab == "img2img":
            dir_name = opts.outdir_img2img_samples.split("/")[-1]
        elif tab == "txt2img-grids":
            dir_name = opts.outdir_txt2img_grids.split("/")[-1]
        elif tab == "img2img-grids":
            dir_name = opts.outdir_img2img_grids.split("/")[-1]
        else:
            dir_name = opts.outdir_extras.split("/")[-1]

        with gr.Row(elem_id=tab + "_connect_images_browser"):
            with gr.Column():
                with gr.Row():
                    with gr.Column(scale=2):
                        with gr.Row():
                            first_page = gr.Button("First Page")
                            prev_page = gr.Button("Prev Page")
                            page_index = gr.Number(value=1, label="Page Index")
                            next_page = gr.Button("Next Page")
                            end_page = gr.Button("End Page")
                        history_gallery = gr.Gallery(
                            show_label=False,
                            elem_id=tab + "_connect_image_gallery",
                        ).style(grid=6)
                        # with gr.Row() as delete_panel:
                        #     with gr.Column(scale=1):
                        #         delete_num = gr.Number(value=1, interactive=True, label="delete next")
                        #     with gr.Column(scale=3):
                        #         delete = gr.Button('Delete', elem_id=tabname + "_images_history_del_button")

                    with gr.Column():
                        with gr.Row():
                            connection_selector = gr.Radio(
                                value="0",
                                choices=["0"],
                                label="Connector",
                                interactive=True,
                            )
                            connection_type = gr.Radio(
                                value="SMB",
                                choices=["SMB", "SFTP"],
                                label="Connection Type",
                            )
                            refetch = gr.Button("Refetch")

                        with gr.Row():
                            with gr.Column():
                                img_file_info = gr.Textbox(
                                    label="Generate Info",
                                    interactive=False,
                                    lines=6,
                                )
                                img_file_name = gr.Textbox(
                                    value="",
                                    label="File Name",
                                    interactive=False,
                                )
                                # img_file_time= gr.HTML()

                        # with gr.Row():
                        #     collected_warning = gr.HTML()

                        #                 # hiden items (Gradio State)
                        with gr.Row(visible=False):
                            tabname_box = gr.Textbox(tab)
                            image_index = gr.Textbox(value="-1")
                            clicked_image_state = gr.Number(value=-1)
                            set_index = gr.Button(
                                "set_index",
                                elem_id=tab + "_connect_browser_set_index",
                            )
                            filenames = gr.State([])

                            images_info = gr.State([])
                            turn_page_switch = gr.Number(
                                value=1, label="turn_page_switch"
                            )  # use as dispatcher for pages change
                            dirname_box = gr.Textbox(
                                value=dir_name, label="dirname_box"
                            )
                            connector_selector_state = gr.Number(
                                value=1, label="connector_selector_state"
                            )  # use as dispatcher for pages change
                            renew_connect = gr.Number(value=1, label="renew_connect")
                            max_page_index_num = gr.Number(
                                value=1, label="max_page_index_box"
                            )

        with gr.Row():
            warning_box = gr.HTML()

        # turn page
        first_page.click(
            lambda s: (1, -s),
            inputs=[turn_page_switch],
            outputs=[page_index, turn_page_switch],
        )
        next_page.click(
            lambda p, s: (p + 1, -s),
            inputs=[page_index, turn_page_switch],
            outputs=[page_index, turn_page_switch],
        )
        prev_page.click(
            lambda p, s: (p - 1, -s),
            inputs=[page_index, turn_page_switch],
            outputs=[page_index, turn_page_switch],
        )
        end_page.click(
            lambda s: (-1, -s),
            inputs=[turn_page_switch],
            outputs=[page_index, turn_page_switch],
        )
        page_index.submit(
            lambda s: -s, inputs=[turn_page_switch], outputs=[turn_page_switch]
        )

        # Select Connector
        connection_type.change(
            lambda s, v: self.get_connetor(s, v),
            inputs=[connection_type, connector_selector_state],
            outputs=[connector_selector_state],
        )
        connector_selector_state.change(
            lambda s: self.get_connector_no(s),
            inputs=[connection_type],
            outputs=[connection_selector],
        )
        connection_selector.change(
            lambda s, v: self.change_connector(s, v),
            inputs=[connection_selector, renew_connect],
            outputs=[renew_connect],
        )
        renew_connect.change(
            lambda s, v: self.get_connetor(s, v),
            inputs=[connection_type, connector_selector_state],
            outputs=[connector_selector_state],
        )

        connection_selector.change(
            fn=self.get_image_page,
            inputs=[dirname_box, page_index],
            outputs=[
                history_gallery,
                page_index,
                warning_box,
                max_page_index_num,
                images_info,
                filenames,
            ],
        )
        refetch.click(
            fn=self.get_image_page,
            inputs=[dirname_box, page_index],
            outputs=[
                history_gallery,
                page_index,
                warning_box,
                max_page_index_num,
                images_info,
                filenames,
            ],
        )
        refetch.click(lambda: print("Refecth"))

        turn_page_switch.change(
            fn=self.get_image_page,
            inputs=[dirname_box, page_index],
            outputs=[
                history_gallery,
                page_index,
                warning_box,
                max_page_index_num,
                images_info,
                filenames,
            ],
        )
        set_index.click(
            fn=None,
            _js="images_history_get_current_img",
            inputs=[tabname_box, page_index, clicked_image_state],
            outputs=[image_index, clicked_image_state],
        )
        clicked_image_state.change(
            fn=self.set_image_info,
            inputs=[image_index, images_info, filenames],
            outputs=[img_file_info, img_file_name],
        )

    def set_image_info(
        self,
        image_index: str,
        imgs_info_arr: List[Dict[str, str]],
        file_names_arr: List[str],
    ) -> Tuple[str, str]:
        """Set image info to to gradio elements."""
        img: str = imgs_info_arr[int(image_index)]["parameters"]
        file_name = file_names_arr[int(image_index)]
        return img, file_name

    def get_image_page(
        self, img_path: str, page_index_param: str
    ) -> Tuple[List[np.ndarray], str, str, int, List[Dict[str, str]], List[str]]:
        """Update the current image page."""
        time = time_lib.time()
        load_info = "<div style='color:#999' align='center'>"
        load_info += "No connection found"
        load_info += "</div>"
        if self.connector is None:
            print("No connector found")
            return [], "1", load_info, 1, [], []
        # off set
        filenames = self.connector.traverse(img_path)[::-1]
        page_index: int = int(page_index_param)  # Force Castiong
        length = len(filenames)
        max_page_index = length // self.num_images_per_page + 1

        """
        boudary check for index
        """
        page_index = max_page_index if page_index == -1 else page_index
        page_index = 1 if page_index < 1 else page_index
        page_index = max_page_index if page_index > max_page_index else page_index
        idx_frm = (page_index - 1) * self.num_images_per_page

        print("page_index: ", page_index)
        print("length: ", length)
        print("max_page_index: ", max_page_index)

        # actual images to show
        image_list_path = filenames[idx_frm : idx_frm + self.num_images_per_page]

        image_list = [self.connector.download(img) for img in image_list_path]
        img_data = [img[0] for img in image_list]

        img_info = [img[1] for img in image_list]

        visible_num = (
            self.num_images_per_page
            if idx_frm + self.num_images_per_page < length
            else length % self.num_images_per_page
        )
        visible_num = self.num_images_per_page if visible_num == 0 else visible_num

        load_info = "<div style='color:#999' align='center'>"
        load_info += f"{length} images in this directory, divided into {int((length + 1) // self.num_images_per_page  + 1)} pages"
        load_info += "</div>"
        print("time: ", time_lib.time() - time)
        return (
            img_data,
            str(page_index),
            load_info,
            max_page_index,
            img_info,
            image_list_path,
        )
