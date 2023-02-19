import customtkinter
import os
from PIL import Image
from tkinter.messagebox import showerror
import copy
import json
from customtkinter import filedialog
import copy
import data_parser as dp


class MassDamping:
    def load_images(self) -> None:
        image_path = os.path.join(os.getcwd(), "icons")
        self.submit_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "submit.png"))
        )

    def __init__(self, mass_damping_frame, servers: list[dict]) -> None:
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
        servers: dict = copy.deepcopy(self.servers)
        payload = list()
        try:
            price = float(self.md_all_servers_certain_price_entry.get())
        except ValueError:
            showerror(title="Error", message="Wrong gold price")
            return
        gold_amount = dp.get_gold_amount()
        for server_id in [list(server.values())[0] for server in servers]:
            payload.append({f"offers[{server_id}][1][price]": f"{price}"})
            payload.append(
                {
                    f"offers[{server_id}][1][amount]": gold_amount[
                        f"offers[{server_id}][1][amount]"
                    ]
                }
            )
            payload.append({f"offers[{server_id}][2][price]": f"{price}"})
            payload.append(
                {
                    f"offers[{server_id}][2][amount]": gold_amount[
                        f"offers[{server_id}][2][amount]"
                    ]
                }
            )
        print(payload)
