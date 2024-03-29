import customtkinter
import os
from PIL import Image
from tkinter.messagebox import showerror
import copy
import json
from customtkinter import filedialog
import requests_worker
import price_calc
import logging
import time
import playsound


class ChainServersRow:
    def combobox_on_text_enter(self, *args, **kwargs):
        if (
            self.csf_add_servers_combobox.get() is None
            or not self.csf_add_servers_combobox.get()
        ):
            self.csf_add_servers_combobox.configure(values=self.servers_labels)
            return
        self.csf_add_servers_combobox.configure(
            values=[
                value
                for value in self.servers_labels
                if self.csf_add_servers_combobox.get().lower() in value.lower()
            ]
        )

    def __init__(
        self,
        chain_servers_frame: customtkinter.CTkFrame,
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
        self.chain_servers_frame = chain_servers_frame
        self.servers = servers
        with open(os.path.join(os.getcwd(), "data", "aliases.json")) as f:
            self.aliases = json.load(f)
        self.csf_add_servers_label = customtkinter.CTkLabel(
            self.chain_servers_frame,
            corner_radius=0,
            height=20,
            width=140,
            font=customtkinter.CTkFont(size=12),
            text=f"None",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
        )
        self.csf_add_servers_label.grid(
            row=self.row, column=0, sticky="ew", ipadx=10, ipady=5
        )

        self.servers_labels = [list(val.keys())[0] for val in self.servers]
        self.csf_add_servers_combobox = customtkinter.CTkComboBox(
            self.chain_servers_frame,
            corner_radius=0,
            height=28,
            font=customtkinter.CTkFont(size=15),
            text_color=("gray10", "gray90"),
            values=self.servers_labels,
            border_width=1,
        )
        self.csf_add_servers_combobox.grid(row=self.row, column=1, sticky="ew")
        self.csf_add_servers_combobox.bind("<KeyRelease>", self.combobox_on_text_enter)
        self.csf_add_servers_combobox.set(
            self.servers_labels[0] if self.servers_labels else "None"
        )
        self.csf_choose_side_combobox = customtkinter.CTkComboBox(
            self.chain_servers_frame,
            corner_radius=0,
            height=28,
            width=140,
            font=customtkinter.CTkFont(size=15),
            text_color=("gray10", "gray90"),
            state="readonly",
            values=["Альянс", "Орда"],
            border_width=1,
        )
        self.csf_choose_side_combobox.set("Сторона")
        self.csf_choose_side_combobox.grid(
            row=self.row, column=2, sticky="ew", padx=(10, 0)
        )

        self.csf_add_button = customtkinter.CTkButton(
            self.chain_servers_frame,
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
        self.csf_add_button.grid(row=self.row, column=3, sticky="ew", padx=5)

        self.csf_gold_amount_entry = customtkinter.CTkEntry(
            self.chain_servers_frame,
            placeholder_text="Enter Gold Amount",
            corner_radius=0,
            font=customtkinter.CTkFont(size=15),
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            height=28,
            border_width=1,
        )
        self.csf_gold_amount_entry.grid(row=self.row, column=4, sticky="ew", padx=5)

        self.csf_gold_price_entry = customtkinter.CTkEntry(
            self.chain_servers_frame,
            placeholder_text="Enter Gold Price",
            corner_radius=0,
            font=customtkinter.CTkFont(size=15),
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            height=28,
            border_width=1,
        )
        self.csf_gold_price_entry.grid(
            row=self.row, column=5, sticky="ew", padx=5, pady=5
        )

        self.csf_submit_button = customtkinter.CTkButton(
            self.chain_servers_frame,
            corner_radius=0,
            height=20,
            width=30,
            font=customtkinter.CTkFont(size=15),
            text="Submit",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            image=self.csf_submit_image,
            command=self.submit_button_on_click,
        )
        self.csf_submit_button.grid(row=self.row, column=6, sticky="ew", padx=5)

        self.csf_save_button = customtkinter.CTkButton(
            self.chain_servers_frame,
            corner_radius=0,
            height=20,
            width=30,
            font=customtkinter.CTkFont(size=15),
            text="Save",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            image=self.csf_save_image,
            command=self.save_button_on_click,
        )
        self.csf_save_button.grid(row=self.row, column=7, sticky="ew", padx=5)

        self.csf_load_button = customtkinter.CTkButton(
            self.chain_servers_frame,
            corner_radius=0,
            height=20,
            width=30,
            font=customtkinter.CTkFont(size=15),
            text="Load",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            image=self.csf_save_image,
            command=self.load_button_on_click,
        )
        self.csf_load_button.grid(row=self.row, column=8, sticky="ew", padx=5)

        self.csf_clear_button = customtkinter.CTkButton(
            self.chain_servers_frame,
            corner_radius=0,
            height=20,
            width=30,
            font=customtkinter.CTkFont(size=15),
            text="Clear",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            image=self.csf_clear_image,
            command=self.clear_button_on_click,
        )
        self.csf_clear_button.grid(row=self.row, column=9, sticky="ew", padx=5)

    def update_added_servers_label(self) -> None:
        servers = [
            f"{self.aliases[list(server.keys())[0]]}({server['side'][0]})"
            for server in self.selected
        ]
        servers_count = 3
        chunks_len = len(servers) // servers_count + 1
        chunks = list()
        for i in range(chunks_len):
            chunks.append(
                servers[i * servers_count : i * servers_count + servers_count]
            )
        chunk_text = list()
        for chunk in chunks:
            chunk_text.append(" | ".join(server for server in chunk))
        text = "\n".join(servers for servers in chunk_text).strip()
        self.csf_add_servers_label.configure(text=text)

    def add_button_on_click(self) -> None:
        added_server = self.csf_add_servers_combobox.get().strip()
        servers = copy.deepcopy(self.servers)
        for server in servers:
            if server.get(added_server) is not None:
                if self.csf_choose_side_combobox.get() == "Сторона":
                    showerror(title="Error", message="Choose side")
                    return

                server["side"] = self.csf_choose_side_combobox.get()
                if server in self.selected:
                    showerror(title="Error", message="Server already selected")
                    return
                self.selected.append(server)
        self.update_added_servers_label()

    def prepare_data(self, silent: bool = False) -> list:
        if self.csf_gold_amount_entry.get():
            try:
                self.gold_amount = int(self.csf_gold_amount_entry.get())
            except ValueError as ex:
                if not silent:
                    showerror(title="Error", message="Wrong gold amount")
                return None
        else:
            self.gold_amount = None
        try:
            self.gold_price = float(self.csf_gold_price_entry.get())
        except ValueError as ex:
            if not silent:
                showerror(title="Error", message="Wrong gold price")
            return None
        if not self.selected:
            if not silent:
                showerror(title="Error", message="No servers selected")
            return None
        return [self.gold_amount, self.gold_price, self.selected]

    def submit_button_on_click(self) -> None:
        raw_data = self.prepare_data()
        data = dict()
        for server in raw_data[2]:
            if raw_data[0] is not None:
                data[
                    f"offers[{list(server.values())[0]}][{'1' if list(server.values())[1]=='Альянс' else '2'}][amount]"
                ] = raw_data[0]
            data[
                f"offers[{list(server.values())[0]}][{'1' if list(server.values())[1]=='Альянс' else '2'}][price]"
            ] = price_calc.get_initial_price(raw_data[1])

        payload = requests_worker.form_payload(data)
        requests_worker.send_request(payload)
        playsound.playsound(
            os.path.join(os.getcwd(), "sounds", "notification_sound.mp3"), False
        )

    def save_button_on_click(self) -> None:
        data = self.prepare_data()
        if not data:
            return
        try:
            with filedialog.asksaveasfile(
                initialdir=os.path.join(os.getcwd(), "saves"),
                initialfile="Untitled.json",
                defaultextension=".json",
                filetypes=[("Json Documents", "*.json")],
            ) as file:
                json.dump(
                    {"amount": data[0], "price": data[1], "servers": data[2]},
                    file,
                    indent=4,
                )
        except AttributeError:
            return
        except:
            logging.exception(time.strftime("[%Y-%m-%d %H:%M:%S]"))
            return

    def load_button_on_click(self) -> None:
        try:
            with filedialog.askopenfile(
                initialdir=os.path.join(os.getcwd(), "saves"),
                filetypes=[("Json Documents", "*.json")],
                defaultextension=".json",
            ) as json_file:
                data = json.load(json_file)
        except:
            logging.exception(time.strftime("[%Y-%m-%d %H:%M:%S]"))
            return
        self.selected = data["servers"]
        self.update_added_servers_label()
        self.csf_gold_amount_entry.delete(0, len(self.csf_gold_amount_entry.get()))
        self.csf_gold_price_entry.delete(0, len(self.csf_gold_price_entry.get()))
        self.csf_gold_amount_entry.insert(
            0, str(data["amount"]) if data["amount"] is not None else ""
        )
        self.csf_gold_price_entry.insert(0, str(data["price"]))

    def clear(self) -> None:
        self.selected = list()
        self.csf_add_servers_label.destroy()
        self.csf_add_servers_label = customtkinter.CTkLabel(
            self.chain_servers_frame,
            corner_radius=0,
            height=20,
            width=100,
            font=customtkinter.CTkFont(size=12),
            text=f"None",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
        )
        self.csf_add_servers_label.grid(
            row=self.row, column=0, sticky="ew", ipadx=10, ipady=5
        )
        self.servers_labels = [list(val.keys())[0] for val in self.servers]
        self.csf_add_servers_combobox = customtkinter.CTkComboBox(
            self.chain_servers_frame,
            corner_radius=0,
            height=28,
            font=customtkinter.CTkFont(size=15),
            text_color=("gray10", "gray90"),
            values=self.servers_labels,
            border_width=1,
        )
        self.csf_add_servers_combobox.bind("<KeyRelease>", self.combobox_on_text_enter)
        self.csf_add_servers_combobox.set(
            self.servers_labels[0] if self.servers_labels else "None"
        )
        self.csf_add_servers_combobox.grid(row=self.row, column=1, sticky="ew")
        self.csf_choose_side_combobox = customtkinter.CTkComboBox(
            self.chain_servers_frame,
            corner_radius=0,
            height=28,
            font=customtkinter.CTkFont(size=15),
            text_color=("gray10", "gray90"),
            state="readonly",
            values=["Альянс", "Орда"],
            border_width=1,
        )
        self.csf_choose_side_combobox.set("Сторона")
        self.csf_choose_side_combobox.grid(
            row=self.row, column=2, sticky="ew", padx=(10, 0)
        )
        self.csf_add_button = customtkinter.CTkButton(
            self.chain_servers_frame,
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
        self.csf_add_button.grid(row=self.row, column=3, sticky="ew", padx=5)

        self.csf_gold_amount_entry = customtkinter.CTkEntry(
            self.chain_servers_frame,
            placeholder_text="Enter Gold Amount",
            corner_radius=0,
            font=customtkinter.CTkFont(size=15),
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            height=28,
            border_width=1,
        )
        self.csf_gold_amount_entry.grid(row=self.row, column=4, sticky="ew", padx=5)

        self.csf_gold_price_entry = customtkinter.CTkEntry(
            self.chain_servers_frame,
            placeholder_text="Enter Gold Price",
            corner_radius=0,
            font=customtkinter.CTkFont(size=15),
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            height=28,
            border_width=1,
        )
        self.csf_gold_price_entry.grid(
            row=self.row, column=5, sticky="ew", padx=5, pady=5
        )

        self.csf_submit_button = customtkinter.CTkButton(
            self.chain_servers_frame,
            corner_radius=0,
            height=20,
            width=30,
            font=customtkinter.CTkFont(size=15),
            text="Submit",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            image=self.csf_submit_image,
            command=self.submit_button_on_click,
        )
        self.csf_submit_button.grid(row=self.row, column=6, sticky="ew", padx=5)

        self.csf_save_button = customtkinter.CTkButton(
            self.chain_servers_frame,
            corner_radius=0,
            height=20,
            width=30,
            font=customtkinter.CTkFont(size=15),
            text="Save",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            image=self.csf_save_image,
            command=self.save_button_on_click,
        )
        self.csf_save_button.grid(row=self.row, column=7, sticky="ew", padx=5)

        self.csf_load_button = customtkinter.CTkButton(
            self.chain_servers_frame,
            corner_radius=0,
            height=20,
            width=30,
            font=customtkinter.CTkFont(size=15),
            text="Load",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            image=self.csf_save_image,
            command=self.load_button_on_click,
        )
        self.csf_load_button.grid(row=self.row, column=8, sticky="ew", padx=5)

        self.csf_clear_button = customtkinter.CTkButton(
            self.chain_servers_frame,
            corner_radius=0,
            height=20,
            width=30,
            font=customtkinter.CTkFont(size=15),
            text="Clear",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            image=self.csf_clear_image,
            command=self.clear_button_on_click,
        )
        self.csf_clear_button.grid(row=self.row, column=9, sticky="ew", padx=5)

    def clear_button_on_click(self) -> None:
        self.clear()

    def load_images(self) -> None:
        image_path = os.path.join(os.getcwd(), "icons")
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
        self.csf_clear_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "csf_clear.png"))
        )

    def destroy(self):
        self.csf_add_button.destroy()
        self.csf_add_servers_combobox.destroy()
        self.csf_add_servers_label.destroy()
        self.csf_choose_side_combobox.destroy()
        self.csf_clear_button.destroy()
        self.csf_submit_button.destroy()
        self.csf_load_button.destroy()
        self.csf_save_button.destroy()
        self.csf_gold_amount_entry.destroy()
        self.csf_gold_price_entry.destroy()

    def represent(self) -> dict:
        if self.csf_gold_amount_entry.get():
            try:
                self.gold_amount = int(self.csf_gold_amount_entry.get())
            except ValueError as ex:
                return None
        else:
            self.gold_amount = None
        try:
            self.gold_price = float(self.csf_gold_price_entry.get())
        except ValueError as ex:
            return None
        if not self.selected:
            showerror(title="Error", message="No servers selected")
            return None
        raw_data = [self.gold_amount, self.gold_price, self.selected]
        data = dict()
        for server in raw_data[2]:
            if raw_data[0] is not None:
                data[
                    f"offers[{list(server.values())[0]}][{'1' if list(server.values())[1]=='Альянс' else '2'}][amount]"
                ] = raw_data[0]
            data[
                f"offers[{list(server.values())[0]}][{'1' if list(server.values())[1]=='Альянс' else '2'}][price]"
            ] = price_calc.get_initial_price(raw_data[1])
        return data
