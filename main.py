import tkinter
import customtkinter
import os
import data_parser as dp
import fp_exceptions as fe
import cookies_worker as cw
from tkinter.messagebox import showerror, showwarning, showinfo
from PIL import Image
import selenium.common.exceptions as selenium_exception
import json

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme(
    "dark-blue"
)  # Themes: "blue" (standard), "green", "dark-blue"
DIRECTORIES = ["data", "downloads"]
customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme(
    "blue"
)  # Themes: blue (default), dark-blue, green


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
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
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)
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
