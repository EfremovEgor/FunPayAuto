import customtkinter
import os
import data_parser as dp
import fp_exceptions as fe
import cookies_worker as cw
from tkinter.messagebox import showerror, showwarning, showinfo
from PIL import Image
import selenium.common.exceptions as selenium_exception
import json


DIRECTORIES = ["data", "downloads"]
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.minimal_gold = 5.0
        self.title("FunPay")
        self.geometry("700x450")
        self.resizable(False, False)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
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
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(7, weight=1)
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
        self.servers = dp.get_servers()
        self.combobox_1 = customtkinter.CTkComboBox(
            self.navigation_frame,
            corner_radius=0,
            font=customtkinter.CTkFont(size=15),
            text_color=("gray10", "gray90"),
            state="readonly",
            values=self.servers,
        )

        self.combobox_1.set("Choose server")
        self.combobox_1.grid(row=7, column=0)

    def submit_min_gold_button_on_click(self):
        try:
            float(self.min_value_entry.get())
        except ValueError as ex:
            showerror(title="Error", message=str(ex))
            return
        self.minimal_gold = float(self.min_value_entry.get())
        self.min_buyout_label.configure(text=f"Current Value {self.minimal_gold}")

    def config_button_on_click(self):
        config_dict = {
            "base_site_url": "https://funpay.com/",
            "goods_page_url": "https://funpay.com/chips/2/",
            "cookies_path": "data\\cookies.json",
        }
        with open(os.path.join(os.getcwd(), "config.json"), "w") as file:
            json.dump(config_dict, file, indent=4)

    def status_button_on_click(self):
        try:
            dp.check_connection()
        except fe.ConfigNotFoundError as ex:
            showerror(
                title="Error",
                message=str(ex)
                + "\n\nTry resetting or creating config file by pressing Create/Reset config button.",
            )
            return
        except fe.CookiesFileNotFoundError as ex:
            showerror(
                title="Error",
                message=str(ex)
                + "\n\nTry pressing Login button and login into your FP account.",
            )
            return
        except fe.AuthenticationError as ex:
            showerror(
                title="Error",
                message=str(ex)
                + "\n\nProbably cookies are old. Try pressing Login button and login into your FP account again.",
            )
            return
        except BaseException as ex:
            showerror(title="Error", message=str(ex))
            return
        showinfo(title="OK", message="Everything is ok.")

    def login_button_on_click(self):
        try:
            cookies = cw.get_cookies()

        except selenium_exception.NoSuchWindowException:
            showwarning(
                title="Warning",
                message="Login window was closed manually, please wait until it is closed automatically.",
            )
            return
        except selenium_exception.TimeoutException:
            showwarning(
                title="Warning",
                message="Login window was closed automatically, because of inactivity or some error.",
            )
            return
        cw.save_cookies(cookies)


def create_directories():
    for dir in DIRECTORIES:
        if not os.path.exists(os.path.join(os.getcwd(), dir)):
            os.mkdir(os.path.join(os.getcwd(), dir))


if __name__ == "__main__":
    app = App()
    create_directories()
    app.mainloop()
