import customtkinter
import os
from PIL import Image
from tkinter.messagebox import showerror
import requests_worker
import price_calc
import logging
import time
import playsound


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

        self.md_any_server_any_side_combobox = customtkinter.CTkComboBox(
            self.mass_damping_frame,
            corner_radius=0,
            height=28,
            font=customtkinter.CTkFont(size=15),
            text_color=("gray10", "gray90"),
            state="readonly",
            values=["Любой(Любой)", "Любой(Альянс)", "Любой(Орда)", "Все"],
            border_width=1,
        )
        self.md_any_server_any_side_combobox.grid(row=2, column=0, sticky="ew", padx=5)
        self.md_any_server_any_side_combobox.set("Любой(Любой)")

        self.md_any_server_any_side_certain_price_entry = customtkinter.CTkEntry(
            self.mass_damping_frame,
            placeholder_text="Enter Gold Price",
            corner_radius=0,
            font=customtkinter.CTkFont(size=15),
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            height=28,
            border_width=1,
        )
        self.md_any_server_any_side_certain_price_entry.grid(
            row=2, column=2, sticky="ew", padx=5
        )
        self.md_any_server_any_side_certain_amount_entry = customtkinter.CTkEntry(
            self.mass_damping_frame,
            placeholder_text="Enter Gold Amount",
            corner_radius=0,
            font=customtkinter.CTkFont(size=15),
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            height=28,
            border_width=1,
        )
        self.md_any_server_any_side_certain_amount_entry.grid(
            row=2, column=1, sticky="ew", padx=5
        )
        self.md_any_server_any_side_certain_price_button = customtkinter.CTkButton(
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
            command=self.md_any_server_any_side_certain_price_button_on_click,
        )
        self.md_any_server_any_side_certain_price_button.grid(
            row=2, column=3, sticky="ew", padx=5
        )

    def md_any_server_any_side_certain_price_button_on_click(self) -> None:
        try:
            price = float(self.md_any_server_any_side_certain_price_entry.get())
        except ValueError:
            showerror(title="Error", message="Wrong gold price")
            return
        try:
            if self.md_any_server_any_side_certain_amount_entry.get():
                amount = int(self.md_any_server_any_side_certain_amount_entry.get())
            else:
                amount = None
        except ValueError:
            showerror(title="Error", message="Wrong gold amount")
            return
        sides = {"Любой(Любой)": 29, "Любой(Альянс)": 1, "Любой(Орда)": 2}
        selected_side = self.md_any_server_any_side_combobox.get()

        if selected_side == "Все":
            data = dict()
            for i in list(sides.values()):
                data[f"offers[375][{i}][price]"] = str(price)
                if amount is not None:
                    data[f"offers[375][{i}][amount]"] = str(amount)
        else:
            data = {f"offers[375][{sides[selected_side]}][price]": str(price)}
            if amount is not None:
                data.update(
                    {f"offers[375][{sides[selected_side]}][amount]": str(amount)}
                )
        print(data, amount)
        payload = requests_worker.form_payload(data)
        requests_worker.send_request(payload)
        playsound.playsound(
            os.path.join(os.getcwd(), "sounds", "notification_sound.mp3"), False
        )

    def md_all_servers_certain_price_button_on_click(self) -> None:
        try:
            price = float(self.md_all_servers_certain_price_entry.get())
        except ValueError:
            showerror(title="Error", message="Wrong gold price")
            return
        try:
            if self.md_all_servers_certain_amount_entry.get():
                amount = int(self.md_all_servers_certain_amount_entry.get())
            else:
                amount = None
        except ValueError:
            showerror(title="Error", message="Wrong gold amount")
            return

        payload = requests_worker.form_payload()
        for key in list(payload.keys()):
            if "amount" in key and amount is not None:
                payload[key] = str(amount)
            if "price" in key:
                payload[key] = str(price_calc.get_initial_price(price))
        requests_worker.send_request(payload)
        playsound.playsound(
            os.path.join(os.getcwd(), "sounds", "notification_sound.mp3"), False
        )
