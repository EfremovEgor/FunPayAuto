import customtkinter
import os
import data_parser as dp
from chain_servers_row import ChainServersRow
import cookies_worker as cw
from tkinter.messagebox import showerror, showwarning, showinfo
from PIL import Image
import selenium.common.exceptions as selenium_exception
import json
import logging
import time
import csv


DIRECTORIES = ["data", "downloads", "logs"]
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):
    def load_images(self):
        image_path = os.path.join(os.getcwd(), "icons")
        self.home_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "login.png"))
        )
        self.config_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "config.png"))
        )
        self.status_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "status.png"))
        )
        self.submit_min_gold_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "submit_min_gold.png"))
        )
        self.reload_servers_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "reload_servers.png"))
        )
        self.add_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "add.png"))
        )
        self.csf_save_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "csf_save.png"))
        )
        self.csf_submit_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "csf_submit.png"))
        )
        self.csf_load_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "csf_load.png"))
        )

    def prepare_navigation_frame(self):
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(9, weight=1)
        # Essentials section
        self.login_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            font=customtkinter.CTkFont(size=15),
            border_spacing=10,
            text="Login",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            image=self.home_image,
            command=self.login_button_on_click,
        )
        self.login_button.grid(row=1, column=0, sticky="ew")
        self.status_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            font=customtkinter.CTkFont(size=15),
            border_spacing=10,
            text="Status",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            image=self.status_image,
            command=self.status_button_on_click,
        )
        self.status_button.grid(row=2, column=0, sticky="ew")
        self.config_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            font=customtkinter.CTkFont(size=15),
            border_spacing=10,
            text="Reset Config"
            if os.path.exists(os.path.join(os.getcwd(), "config.json"))
            else "Create Config",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            image=self.config_image,
            command=self.config_button_on_click,
        )
        self.config_button.grid(row=3, column=0, sticky="ew")
        # Gold values section
        self.min_value_entry = customtkinter.CTkEntry(
            self.navigation_frame,
            placeholder_text="Enter minimal gold",
            corner_radius=0,
            font=customtkinter.CTkFont(size=15),
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            height=40,
        )
        self.min_value_entry.grid(row=5, column=0, sticky="ew")
        self.submit_min_gold_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            font=customtkinter.CTkFont(size=15),
            border_spacing=10,
            text="Submit",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            image=self.submit_min_gold_image,
            command=self.submit_min_gold_button_on_click,
        )
        self.submit_min_gold_button.grid(row=6, column=0, sticky="ew")
        self.min_buyout_label = customtkinter.CTkLabel(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            font=customtkinter.CTkFont(size=15),
            text=f"Current Value {self.minimal_gold}",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
        )
        self.min_buyout_label.grid(row=4, column=0, sticky="ew")
        self.csf_select_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            font=customtkinter.CTkFont(size=15),
            border_spacing=10,
            text="Chain Servers",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            image=self.status_image,
            command=self.csf_select_button_on_click,
        )
        self.csf_select_button.grid(row=7, column=0, sticky="ew")
        self.md_select_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            font=customtkinter.CTkFont(size=15),
            border_spacing=10,
            text="Mass Damping",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            image=self.status_image,
            command=self.md_select_button_on_click,
        )
        self.md_select_button.grid(row=8, column=0, sticky="ew")

    def prepare_chain_servers_frame(self):
        n_rows = 10
        self.chain_servers_frame = customtkinter.CTkFrame(
            self, corner_radius=0, fg_color="transparent"
        )
        self.chain_servers_frame.grid_columnconfigure(8, weight=1)
        self.chain_servers_frame.rowconfigure(n_rows + 1, weight=1)
        self.csf_label = customtkinter.CTkLabel(
            self.chain_servers_frame,
            corner_radius=0,
            height=40,
            font=customtkinter.CTkFont(size=30),
            text=f"Chain Servers",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
        )

        self.csf_label.grid(row=0, column=1, sticky="ew")

        self.csf_rows = list()
        for row in range(n_rows):
            self.csf_rows.append(
                ChainServersRow(
                    chain_servers_frame=self.chain_servers_frame, row=row + 1
                )
            )

    def prepare_mass_damping(self):
        self.mass_damping_frame = customtkinter.CTkFrame(
            self, corner_radius=0, fg_color="transparent"
        )
        self.mass_damping_frame.grid_columnconfigure(8, weight=1)
        self.mass_damping_frame.rowconfigure(10, weight=1)
        self.md_label = customtkinter.CTkLabel(
            self.mass_damping_frame,
            corner_radius=0,
            height=40,
            font=customtkinter.CTkFont(size=30),
            text=f"Mass damping",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
        )

        self.md_label.grid(row=0, column=1, sticky="ew")

    def __init__(self):
        super().__init__()
        self.minimal_gold = 5.0
        self.title("FunPay")
        self.geometry("1200x600")
        self.resizable(False, False)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.load_images()
        self.prepare_navigation_frame()
        self.prepare_chain_servers_frame()
        # Servers section
        # self.servers = list()
        # self.servers_combobox = customtkinter.CTkComboBox(
        #     self.navigation_frame,
        #     corner_radius=0,
        #     font=customtkinter.CTkFont(size=15),
        #     text_color=("gray10", "gray90"),
        #     state="readonly",
        #     values=self.servers,
        # )
        # self.servers_combobox.set("Choose server")
        # self.servers_combobox.grid(row=8, column=0)
        # self.load_servers()
        # self.reupload_servers = customtkinter.CTkButton(
        #     self.navigation_frame,
        #     corner_radius=0,
        #     height=40,
        #     font=customtkinter.CTkFont(size=15),
        #     border_spacing=10,
        #     text="Reload Servers",
        #     fg_color="transparent",
        #     text_color=("gray10", "gray90"),
        #     hover_color=("gray70", "gray30"),
        #     anchor="w",
        #     image=self.reload_servers_image,
        #     command=self.reupload_servers,
        # )
        # self.reupload_servers.grid(row=7, column=0, sticky="ew", pady=(10, 0))
        self.prepare_mass_damping()
        self.select_frame_by_name("mass_damping")

    def csf_select_button_on_click(self):
        self.select_frame_by_name("chain_servers")

    def md_select_button_on_click(self):
        self.select_frame_by_name("mass_damping")

    def select_frame_by_name(self, name):

        # show selected frame
        if name == "chain_servers":
            self.chain_servers_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.chain_servers_frame.grid_forget()
        if name == "mass_damping":
            self.mass_damping_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.mass_damping_frame.grid_forget()
        # if name == "frame_3":
        #     self.third_frame.grid(row=0, column=1, sticky="nsew")
        # else:
        #     self.third_frame.grid_forget()

    def reupload_servers(self):
        try:
            self.servers = dp.get_servers()
        except BaseException as ex:
            logging.exception(time.strftime("[%Y-%m-%d %H:%M:%S]"))
            return
        if not self.servers:
            showwarning(title="Warning", message="No servers found")
            logging.warning(time.strftime("[%Y-%m-%d %H:%M:%S]" + ": No servers found"))
            return
        self.save_servers()
        self.load_servers()

    def submit_min_gold_button_on_click(self) -> None:
        try:
            float(self.min_value_entry.get())
        except ValueError as ex:
            showerror(title="Error", message=str(ex))
            return
        self.minimal_gold = float(self.min_value_entry.get())
        self.min_buyout_label.configure(text=f"Current Value {self.minimal_gold}")

    def load_servers(self) -> None:
        if not os.path.exists(os.path.join(os.getcwd(), "config.json")):
            return
        with open(os.path.join(os.getcwd(), "config.json"), "r") as json_file:
            config = json.load(json_file)
            path = config.get(
                "servers_path", os.path.join(os.getcwd(), "data", "servers.csv")
            )
        if not os.path.exists(path):
            return
        with open(path, mode="r") as servers_file:
            servers_file = csv.reader(servers_file, delimiter=",")
            for row in servers_file:
                self.servers = row if row else self.servers
            self.servers_combobox.configure(values=self.servers)

    def save_servers(self):
        dp.essentials_check(lambda x: x)
        with open(os.path.join(os.getcwd(), "config.json"), "r") as json_file:
            config = json.load(json_file)
            path = config.get(
                "servers_path", os.path.join(os.getcwd(), "data", "servers.csv")
            )
        with open(path, mode="w") as servers_file:
            servers_file = csv.writer(
                servers_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
            )
            servers_file.writerow(self.servers)

    def config_button_on_click(self) -> None:
        config_dict = {
            "base_site_url": "https://funpay.com/",
            "goods_page_url": "https://funpay.com/chips/2/",
            "cookies_path": "data\\cookies.json",
            "servers_path": "data\\servers.csv",
        }
        with open(os.path.join(os.getcwd(), "config.json"), "w") as file:
            json.dump(config_dict, file, indent=4)

    def status_button_on_click(self) -> None:
        try:
            dp.check_connection()
        except BaseException as ex:
            logging.exception(time.strftime("[%Y-%m-%d %H:%M:%S]"))
            return
        showinfo(title="OK", message="Everything is ok.")

    def login_button_on_click(self) -> None:
        try:
            cookies = cw.get_cookies()

        except selenium_exception.NoSuchWindowException:
            showwarning(
                title="Warning",
                message="Login window was closed manually, please wait until it is closed automatically.",
            )
            logging.exception()
            return
        except selenium_exception.TimeoutException:
            showwarning(
                title="Warning",
                message="Login window was closed automatically, because of inactivity or some error.",
            )
            logging.exception()
            return
        cw.save_cookies(cookies)


def create_directories() -> None:
    for dir in DIRECTORIES:
        if not os.path.exists(os.path.join(os.getcwd(), dir)):
            os.mkdir(os.path.join(os.getcwd(), dir))


if __name__ == "__main__":
    create_directories()
    logging.basicConfig(
        filename=os.path.join("logs", f'{time.strftime("%Y_%m_%d-%H_%M_%S")}.log'),
        filemode="w",
        format="%(asctime)s - %(message)s",
        datefmt="%d-%b-%y %H:%M:%S",
    )

    app = App()
    app.mainloop()
