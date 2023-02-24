import customtkinter
import os
from PIL import Image
from tkinter.messagebox import showerror, showinfo
import requests_worker
import price_calc
import copy
import data_parser
import logging
import time
import json


class PreciseDampingRaw:
    def __init__(
        self,
        precise_damping_frame: customtkinter.CTkFrame,
        servers: list[dict],
        row: int = 1,
    ) -> None:
        logging.basicConfig(
            filename=os.path.join("logs", f'{time.strftime("%Y_%m_%d-%H_%M_%S")}.log'),
            filemode="w",
            format="%(asctime)s - %(message)s",
            datefmt="%d-%b-%y %H:%M:%S",
        )
        self.load_images()
        self.selected = list()
        self.row = row
        with open(os.path.join(os.getcwd(), "data", "aliases.json")) as f:
            self.aliases = json.load(f)
        self.precise_damping_frame = precise_damping_frame
        self.servers = servers
        self.data = dict()
        self.pd_add_servers_label = customtkinter.CTkLabel(
            self.precise_damping_frame,
            corner_radius=0,
            height=20,
            width=100,
            font=customtkinter.CTkFont(size=15),
            text=f"None",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
        )
        self.pd_add_servers_label.grid(row=self.row, column=0, sticky="ew", ipadx=10)

        servers = [list(val.keys())[0] for val in self.servers]

        self.pd_add_servers_combobox = customtkinter.CTkComboBox(
            self.precise_damping_frame,
            corner_radius=0,
            height=28,
            font=customtkinter.CTkFont(size=15),
            text_color=("gray10", "gray90"),
            state="readonly",
            values=servers,
            border_width=1,
        )
        self.pd_add_servers_combobox.grid(row=self.row, column=1, sticky="ew", pady=5)

        self.pd_choose_side_combobox = customtkinter.CTkComboBox(
            self.precise_damping_frame,
            corner_radius=0,
            height=28,
            font=customtkinter.CTkFont(size=15),
            text_color=("gray10", "gray90"),
            state="readonly",
            values=["Альянс", "Орда"],
            border_width=1,
        )
        self.pd_choose_side_combobox.set("Сторона")
        self.pd_choose_side_combobox.grid(
            row=self.row, column=2, sticky="ew", padx=(10, 0)
        )

        self.pd_add_button = customtkinter.CTkButton(
            self.precise_damping_frame,
            corner_radius=0,
            height=20,
            width=30,
            font=customtkinter.CTkFont(size=15),
            text="Add",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            image=self.add_image,
            command=self.add_button_on_click,
        )
        self.pd_add_button.grid(row=self.row, column=3, sticky="ew", padx=5)

        self.pd_min_gold_price_entry = customtkinter.CTkEntry(
            self.precise_damping_frame,
            placeholder_text="Enter minimal price",
            corner_radius=0,
            font=customtkinter.CTkFont(size=15),
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            height=28,
            border_width=1,
        )
        self.pd_min_gold_price_entry.grid(
            row=self.row, column=4, sticky="ew", padx=5, pady=5
        )

        self.pd_submit_button = customtkinter.CTkButton(
            self.precise_damping_frame,
            corner_radius=0,
            height=20,
            width=30,
            font=customtkinter.CTkFont(size=15),
            text="Submit",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            image=self.pd_submit_image,
            command=self.submit_button_on_click,
        )
        self.pd_submit_button.grid(row=self.row, column=5, sticky="ew", padx=5)

        self.pd_final_gold_price_entry = customtkinter.CTkEntry(
            self.precise_damping_frame,
            placeholder_text="",
            corner_radius=0,
            font=customtkinter.CTkFont(size=15),
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            height=28,
            border_width=1,
        )
        self.pd_final_gold_price_entry.grid(
            row=self.row, column=6, sticky="ew", padx=5, pady=5
        )

        self.pd_send_button = customtkinter.CTkButton(
            self.precise_damping_frame,
            corner_radius=0,
            height=20,
            width=30,
            font=customtkinter.CTkFont(size=15),
            text="Send",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            image=self.pd_send_image,
            command=self.send_button_on_click,
        )
        self.pd_send_button.grid(row=self.row, column=7, sticky="ew", padx=5)

        self.csf_clear_button = customtkinter.CTkButton(
            self.precise_damping_frame,
            corner_radius=0,
            height=20,
            width=30,
            font=customtkinter.CTkFont(size=15),
            text="Clear",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            image=self.pd_clear_image,
            command=self.clear_button_on_click,
        )
        self.csf_clear_button.grid(row=self.row, column=9, sticky="ew", padx=5)

    def clear_button_on_click(self) -> None:
        self.selected = list()
        self.data = dict()
        self.pd_add_servers_label = customtkinter.CTkLabel(
            self.precise_damping_frame,
            corner_radius=0,
            height=20,
            width=100,
            font=customtkinter.CTkFont(size=15),
            text=f"None",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
        )
        self.pd_add_servers_label.grid(row=self.row, column=0, sticky="ew", ipadx=10)

        servers = [list(val.keys())[0] for val in self.servers]

        self.pd_add_servers_combobox = customtkinter.CTkComboBox(
            self.precise_damping_frame,
            corner_radius=0,
            height=28,
            font=customtkinter.CTkFont(size=15),
            text_color=("gray10", "gray90"),
            state="readonly",
            values=servers,
            border_width=1,
        )
        self.pd_add_servers_combobox.grid(row=self.row, column=1, sticky="ew", pady=5)
        self.pd_add_servers_combobox.set(servers[0])

        self.pd_choose_side_combobox = customtkinter.CTkComboBox(
            self.precise_damping_frame,
            corner_radius=0,
            height=28,
            font=customtkinter.CTkFont(size=15),
            text_color=("gray10", "gray90"),
            state="readonly",
            values=["Альянс", "Орда"],
            border_width=1,
        )
        self.pd_choose_side_combobox.set("Сторона")
        self.pd_choose_side_combobox.grid(
            row=self.row, column=2, sticky="ew", padx=(10, 0)
        )

        self.pd_add_button = customtkinter.CTkButton(
            self.precise_damping_frame,
            corner_radius=0,
            height=20,
            width=30,
            font=customtkinter.CTkFont(size=15),
            text="Add",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            image=self.add_image,
            command=self.add_button_on_click,
        )
        self.pd_add_button.grid(row=self.row, column=3, sticky="ew", padx=5)

        self.pd_min_gold_price_entry = customtkinter.CTkEntry(
            self.precise_damping_frame,
            placeholder_text="Enter minimal price",
            corner_radius=0,
            font=customtkinter.CTkFont(size=15),
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            height=28,
            border_width=1,
        )
        self.pd_min_gold_price_entry.grid(
            row=self.row, column=4, sticky="ew", padx=5, pady=5
        )

        self.pd_submit_button = customtkinter.CTkButton(
            self.precise_damping_frame,
            corner_radius=0,
            height=20,
            width=30,
            font=customtkinter.CTkFont(size=15),
            text="Submit",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            image=self.pd_submit_image,
            command=self.submit_button_on_click,
        )
        self.pd_submit_button.grid(row=self.row, column=5, sticky="ew", padx=5)

        self.pd_final_gold_price_entry = customtkinter.CTkEntry(
            self.precise_damping_frame,
            placeholder_text="",
            corner_radius=0,
            font=customtkinter.CTkFont(size=15),
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            height=28,
            border_width=1,
        )
        self.pd_final_gold_price_entry.grid(
            row=self.row, column=6, sticky="ew", padx=5, pady=5
        )

        self.pd_send_button = customtkinter.CTkButton(
            self.precise_damping_frame,
            corner_radius=0,
            height=20,
            width=30,
            font=customtkinter.CTkFont(size=15),
            text="Send",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            image=self.pd_send_image,
            command=self.send_button_on_click,
        )
        self.pd_send_button.grid(row=self.row, column=7, sticky="ew", padx=5)

        self.csf_clear_button = customtkinter.CTkButton(
            self.precise_damping_frame,
            corner_radius=0,
            height=20,
            width=30,
            font=customtkinter.CTkFont(size=15),
            text="Clear",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            image=self.pd_clear_image,
            command=self.clear_button_on_click,
        )
        self.csf_clear_button.grid(row=self.row, column=9, sticky="ew", padx=5)

    def update_added_servers_label(self) -> None:
        text = " | ".join(
            f"{self.aliases[list(server.keys())[0]]}({server['side'][0]})"
            for server in self.selected
        )
        self.pd_add_servers_label.configure(text=text)

    def add_button_on_click(self) -> None:
        added_server = self.pd_add_servers_combobox.get().strip()
        servers = copy.deepcopy(self.servers)
        for server in servers:
            if server.get(added_server, None) is not None:
                if self.pd_choose_side_combobox.get() == "Сторона":
                    showerror(title="Error", message="Choose side")
                    return

                server["side"] = self.pd_choose_side_combobox.get()
                if server in self.selected:
                    showerror(title="Error", message="Server already selected")
                    return
                self.selected.append(server)
        self.update_added_servers_label()

    def prepare_data(self) -> list:
        try:
            self.min_gold_price = float(self.pd_min_gold_price_entry.get())
        except ValueError as ex:
            showerror(title="Error", message="Wrong gold price")
            return None
        if not self.selected:
            showerror(title="Error", message="No servers selected")
            return None
        return [self.min_gold_price, self.selected]

    def submit_button_on_click(self) -> None:
        try:
            min_price = float(self.pd_min_gold_price_entry.get())
        except ValueError as ex:
            logging.exception(time.strftime("[%Y-%m-%d %H:%M:%S]"))
            showerror(title="Error", message="Wrong gold price")
            return
        raw_data = self.prepare_data()
        try:
            prices = data_parser.get_prices()
        except:
            logging.exception(time.strftime("[%Y-%m-%d %H:%M:%S]"))
            return
        data = dict()
        for server in list(raw_data[1]):
            keys = list(server.keys())

            data[
                f"offers[{list(server.values())[0]}][{'1' if list(server.values())[1]=='Альянс' else '2'}][price]"
            ] = round(
                min(
                    number
                    for number in prices[keys[0], server[keys[1]]]
                    if number > min_price
                )
                - 0.01,
                3,
            )
        self.pd_final_gold_price_entry.delete(
            0, len(self.pd_final_gold_price_entry.get())
        )
        self.pd_final_gold_price_entry.insert(
            0, ",".join([str(val) for val in list(data.values())])
        )
        self.data = data
        message = "\n".join(
            f"{list(server.keys())[0]}({server['side']}) -> {price}"
            for server, price in list(zip(self.selected, list(self.data.values())))
        )
        showinfo(title="Info", message=message)

    def send_button_on_click(self) -> None:
        values = self.pd_final_gold_price_entry.get().strip().split(",")
        if len(values) < len(list(self.data.keys())):
            showerror(title="Error", message="Not enough params")
        for i, key in enumerate(list(self.data.keys())):
            self.data[key] = str(price_calc.get_initial_price(float(values[i])))
        payload = requests_worker.form_payload(self.data)
        try:
            response_code = requests_worker.send_request(payload)
            if response_code != 200:
                raise Exception("Request wasn't sent properly")
        except:
            logging.exception(time.strftime("[%Y-%m-%d %H:%M:%S]"))
            return

    def load_images(self) -> None:
        image_path = os.path.join(os.getcwd(), "icons")
        self.add_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "add.png"))
        )
        self.pd_submit_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "csf_submit.png"))
        )
        self.pd_send_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "pd_send.png"))
        )
        self.pd_clear_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "csf_clear.png"))
        )
