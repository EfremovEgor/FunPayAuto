import customtkinter
import os
from PIL import Image


class ChainServersRow:
    def load_images(self):
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

    def __init__(
        self, chain_servers_frame: customtkinter.CTkFrame, servers: list, row: int = 1
    ) -> None:
        self.load_images()
        self.row = row
        self.chain_servers_frame = chain_servers_frame

        self.csf_add_servers_label = customtkinter.CTkLabel(
            self.chain_servers_frame,
            corner_radius=0,
            height=20,
            width=100,
            font=customtkinter.CTkFont(size=15),
            text=f"None",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
        )
        self.csf_add_servers_label.grid(row=self.row, column=0, sticky="ew", ipadx=10)

        self.csf_add_servers_combobox = customtkinter.CTkComboBox(
            self.chain_servers_frame,
            corner_radius=0,
            height=28,
            font=customtkinter.CTkFont(size=15),
            text_color=("gray10", "gray90"),
            state="readonly",
            values=servers,
            border_width=1,
        )
        self.csf_add_servers_combobox.grid(row=self.row, column=1, sticky="ew")

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
            command=None,
        )
        self.csf_add_button.grid(row=self.row, column=2, sticky="ew", padx=5)

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
        self.csf_gold_amount_entry.grid(row=self.row, column=3, sticky="ew", padx=5)

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
            row=self.row, column=4, sticky="ew", padx=5, pady=5
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
            command=None,
        )
        self.csf_submit_button.grid(row=self.row, column=5, sticky="ew", padx=5)

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
            command=None,
        )
        self.csf_save_button.grid(row=self.row, column=6, sticky="ew", padx=5)

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
            command=None,
        )
        self.csf_load_button.grid(row=self.row, column=7, sticky="ew", padx=5)
