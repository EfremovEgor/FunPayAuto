import customtkinter
import os
from PIL import Image
from tkinter.messagebox import showerror
import requests_worker
import price_calc
import logging
import time


class MassDamping:
    def load_images(self) -> None:
        image_path = os.path.join(os.getcwd(), "icons")
        self.submit_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "submit.png"))
        )

    def __init__(self, mass_damping_frame, servers: list[dict]) -> None:
        logging.basicConfig(
            filename=os.path.join("logs", f'{time.strftime("%Y_%m_%d-%H_%M_%S")}.log'),
            filemode="w",
            format="%(asctime)s - %(message)s",
            datefmt="%d-%b-%y %H:%M:%S",
        )
        self.load_images()
        self.mass_damping_frame = mass_damping_frame
        self.servers = servers
        self.md_all_servers_certain_price_label = customtkinter.CTkLabel(
            self.mass_damping_frame,
            corner_radius=0,
            height=20,
            width=100,
            font=customtkinter.CTkFont(size=15),
            text=f"Set certain price on all servers",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
        )
        self.md_all_servers_certain_price_label.grid(
            row=1, column=0, sticky="ew", ipadx=10
        )
        self.md_all_servers_certain_price_entry = customtkinter.CTkEntry(
            self.mass_damping_frame,
            placeholder_text="Enter Gold Price",
            corner_radius=0,
            font=customtkinter.CTkFont(size=15),
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            height=28,
            border_width=1,
        )
        self.md_all_servers_certain_price_entry.grid(
            row=1, column=2, sticky="ew", padx=5
        )
        self.md_all_servers_certain_amount_entry = customtkinter.CTkEntry(
            self.mass_damping_frame,
            placeholder_text="Enter Gold Amount",
            corner_radius=0,
            font=customtkinter.CTkFont(size=15),
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            height=28,
            border_width=1,
        )
        self.md_all_servers_certain_amount_entry.grid(
            row=1, column=1, sticky="ew", padx=5
        )
        self.md_all_servers_certain_price_button = customtkinter.CTkButton(
            self.mass_damping_frame,
            corner_radius=0,
            height=20,
            width=30,
            font=customtkinter.CTkFont(size=15),
            text="Submit",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            image=self.submit_image,
            command=self.md_all_servers_certain_price_button_on_click,
        )
        self.md_all_servers_certain_price_button.grid(
            row=1, column=3, sticky="ew", padx=5
        )

    def md_all_servers_certain_price_button_on_click(self) -> None:
        try:
            price = float(self.md_all_servers_certain_price_entry.get())
        except ValueError:
            showerror(title="Error", message="Wrong gold price")
            return
        try:
            amount = int(self.md_all_servers_certain_amount_entry.get())
        except ValueError:
            showerror(title="Error", message="Wrong gold amount")
            return
        payload = requests_worker.form_payload()
        for key in list(payload.keys()):
            if "amount" in key:
                payload[key] = str(amount)
            if "price" in key:
                payload[key] = str(price_calc.get_initial_price(price))
        print(payload)
        requests_worker.send_request(payload)
