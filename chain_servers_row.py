import customtkinter
import os
from PIL import Image
from tkinter.messagebox import showerror
import copy


class ChainServersRow:
    def __init__(
        self,
        chain_servers_frame: customtkinter.CTkFrame,
        servers: list[dict],
        row: int = 1,
    ) -> None:
        self.load_images()
        self.selected = list()
        self.row = row
        self.chain_servers_frame = chain_servers_frame
        self.servers = servers
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
        servers = [list(val.keys())[0] for val in self.servers]
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

    def add_button_on_click(self) -> None:
        label_text = self.csf_add_servers_label.cget("text").strip()
        added_server = self.csf_add_servers_combobox.get().strip()
        servers = copy.deepcopy(self.servers)
        for server in servers:
            if server.get(added_server, None) is not None:
                if self.csf_choose_side_combobox.get() == "Сторона":
                    showerror(title="Error", message="Choose side")
                    return

                server["side"] = self.csf_choose_side_combobox.get()
                if server in self.selected:
                    showerror(title="Error", message="Server already selected")
                    return
                self.selected.append(server)

        text = " | ".join(
            f"{list(server.keys())[0]}({server['side']})" for server in self.selected
        )
        self.csf_add_servers_label.configure(text=text)
        # print(self.selected)

    def submit_button_on_click(self) -> None:
        try:
            self.gold_amount = int(self.csf_gold_amount_entry.get())
        except ValueError as ex:
            showerror(title="Error", message="Wrong gold amount")
            return
        try:
            self.gold_price = float(self.csf_gold_price_entry.get())
        except ValueError as ex:
            showerror(title="Error", message="Wrong gold price")
            return
        if not self.selected:
            showerror(title="Error", message="No servers selected")
            return
        print(self.gold_amount, self.gold_price, self.selected)

    def save_button_on_click(self) -> None:
        ...

    def load_button_on_click(self) -> None:
        ...

    def clear_button_on_click(self) -> None:
        self.load_images()
        self.selected = list()
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
        servers = [list(val.keys())[0] for val in self.servers]
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
        self.csf_add_servers_combobox.set(servers[0])
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
        self.csf_clear_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "csf_clear.png"))
        )
