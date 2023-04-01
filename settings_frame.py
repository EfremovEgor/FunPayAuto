import customtkinter
import os
from PIL import Image
from tkinter.messagebox import showerror
import requests_worker
import price_calc
import logging
import time
import playsound
import json


class SettingRow:
    def __init__(
        self, frame: customtkinter.CTkFrame, row: int, value: str, name: str
    ) -> None:
        self.name = name
        text = SettingsObj.aliases[name]
        self.setting_frame = frame
        self.row = row
        self.setting_label = customtkinter.CTkLabel(
            self.setting_frame,
            corner_radius=0,
            height=20,
            width=100,
            font=customtkinter.CTkFont(size=20),
            text=text,
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            anchor="w",
        )
        self.setting_label.grid(row=self.row, column=0, sticky="ew", ipadx=10)
        self.setting_entry = customtkinter.CTkEntry(
            self.setting_frame,
            placeholder_text=value,
            corner_radius=0,
            font=customtkinter.CTkFont(size=15),
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            height=28,
            border_width=1,
        )
        self.setting_entry.grid(row=self.row, column=1, sticky="ew", padx=5, pady=5)

    def destroy(self) -> None:
        self.setting_label.destroy()
        self.setting_entry.destroy()


class SettingsObj:
    aliases: dict = {
        "gold_damp_threshold": "Minimal gold threshold for mass damping:",
        "base_site_url": "Url for the base site:",
        "goods_page_url": "Url for the goods page:",
        "cookies_path": "Cookies path:",
        "servers_path": "Servers path:",
        "trades_page_url": "Url for the trades page:",
    }

    def __init__(self, frame: customtkinter.CTkFrame) -> None:
        logging.basicConfig(
            filename=os.path.join("logs", f'{time.strftime("%Y_%m_%d-%H_%M_%S")}.log'),
            filemode="w",
            format="%(asctime)s - %(message)s",
            datefmt="%d-%b-%y %H:%M:%S",
        )
        self.load_images()
        self.settings_rows: list[SettingRow] = list()
        self.setting_frame = frame
        self.load_current_config()
        self.reload_config_button = customtkinter.CTkButton(
            self.setting_frame,
            corner_radius=0,
            height=40,
            width=40,
            font=customtkinter.CTkFont(size=15),
            text="Reload",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            image=self.reload_image,
            command=self.load_current_config,
        )
        self.reload_config_button.grid(
            row=len(self.settings_rows) + 1, column=1, sticky="w", padx=5
        )
        self.update_settings = customtkinter.CTkButton(
            self.setting_frame,
            corner_radius=0,
            height=40,
            width=40,
            font=customtkinter.CTkFont(size=15),
            text="Update",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            image=self.update_image,
            command=self.update_settings_file,
        )
        self.update_settings.grid(
            row=len(self.settings_rows) + 1, column=0, sticky="e", padx=5
        )

    def update_settings_file(self) -> None:
        for row in self.settings_rows:
            if not row.setting_entry.get().strip():
                continue
            try:
                value = float(row.setting_entry.get().strip())
                if round(value, 10) == int(value):
                    value = int(value)
            except ValueError:
                try:
                    value = float(row.setting_entry.get().strip())

                except ValueError:
                    value = row.setting_entry.get().strip()
            self.config.update({row.name: value})
        with open(os.path.join(os.getcwd(), "config.json"), "w") as file:
            json.dump(self.config, file, indent=4)

    def load_current_config(self) -> None:
        with open(os.path.join(os.getcwd(), "config.json"), "r") as file:
            self.config: dict = json.load(file)
        raw = list()
        for name, value in self.config.items():
            if name in self.aliases.keys():
                raw.append((name, value))
        for row, (name, value) in enumerate(raw, 1):
            self.settings_rows.append(SettingRow(self.setting_frame, row, value, name))

    def load_images(self) -> None:
        image_path = os.path.join(os.getcwd(), "icons")
        self.reload_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "reload.png"))
        )
        self.update_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "submit.png"))
        )
