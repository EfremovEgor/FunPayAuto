import json
import customtkinter
from tkinter import filedialog
import tkinter as tk
import os
from PIL import Image
from data_parser import get_gold_amount
import random
import playsound
import sys

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


def tksleep(self, time: float) -> None:
    """
    Emulating `time.sleep(seconds)`
    Created by TheLizzard, inspired by Thingamabobs
    """
    self.after(int(time * 1000), self.quit)
    self.mainloop()


tk.Misc.tksleep = tksleep


class Row:
    def update_added_servers_label(self) -> None:
        servers = [
            f"{self.aliases[list(server.keys())[0]]}({server['side'][0]})"
            for server in self.selected
        ]
        servers_count = 5
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
        self.servers_label.configure(text=text)

    def __init__(
        self, frame: customtkinter.CTkFrame, row: int, servers: list[dict]
    ) -> None:
        with open(os.path.join(os.getcwd(), "data", "aliases.json")) as f:
            self.aliases = json.load(f)
        self.row = row
        self.frame = frame
        self.selected = servers
        self.servers_label = customtkinter.CTkLabel(
            self.frame,
            corner_radius=0,
            height=20,
            width=100,
            font=customtkinter.CTkFont(size=12),
            text=f"None",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
        )
        self.servers_label.grid(
            row=self.row, column=0, sticky="w", ipadx=10, pady=(0, 10)
        )

        self.minimal_gold_amount = customtkinter.CTkLabel(
            self.frame,
            corner_radius=0,
            height=20,
            width=100,
            font=customtkinter.CTkFont(size=20),
            text=f"None",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            anchor="w",
        )
        self.minimal_gold_amount.grid(
            row=self.row, column=1, sticky="w", ipadx=10, pady=(0, 10)
        )


class App(customtkinter.CTk):
    def load_images(self) -> None:
        image_path = os.path.join(os.getcwd(), "icons")
        self.load_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "csf_load.png"))
        )

    def __init__(self) -> None:
        super().__init__()
        self.load_images()
        self.title("FunPayMetrics")
        self.geometry("800x400")
        self.resizable(True, True)
        self.grid_rowconfigure(100, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.csf_label = customtkinter.CTkLabel(
            self,
            corner_radius=0,
            height=40,
            font=customtkinter.CTkFont(size=30),
            text=f"Metrics",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
        )
        self.csf_label.grid(row=0, column=0, sticky="w")
        self.load_button = customtkinter.CTkButton(
            self,
            corner_radius=0,
            height=40,
            font=customtkinter.CTkFont(size=15),
            border_spacing=10,
            text="Load",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            image=self.load_image,
            command=self.load_button_on_click,
        )
        self.load_button.grid(row=1, column=0, sticky="w")
        self.servers_codes = dict()
        with open(os.path.join(os.getcwd(), "data", "servers.json"), "r") as file:
            for server in json.load(file):
                self.servers_codes.update(
                    {list(server.keys())[0]: list(server.values())[0]}
                )

    def update_gold_amounts(self) -> None:
        self.gold_amounts = get_gold_amount()
        threshold_passed = False
        for row in self.rows:
            raw_amounts = [
                (
                    self.gold_amounts[
                        f"offers[{self.servers_codes[list(server.keys())[0]]}][{ 1 if server['side'] == 'Альянс' else 2 }][amount]"
                    ],
                    list(server.keys())[0],
                    server["side"],
                )
                for server in row.selected
            ]
            amounts = list()
            for server in raw_amounts:
                try:
                    val = int(server[0])

                    amounts.append(server)
                except ValueError:
                    pass
            amounts = min(amounts, key=lambda x: int(x[0]))

            row.minimal_gold_amount.configure(text_color=("gray10", "gray90"))
            row.minimal_gold_amount.configure(
                text=f"{amounts[1]}({amounts[2]}): {amounts[0]}"
            )
            if int(amounts[0]) < 1_000_000:
                row.minimal_gold_amount.configure(text_color="red")
                if not threshold_passed:
                    playsound.playsound(
                        os.path.join(
                            os.getcwd(),
                            "sounds",
                            "the-notification-email-143029.mp3",
                        ),
                        False,
                    )
                    threshold_passed = True

    def load_button_on_click(self) -> None:
        with filedialog.askopenfile(
            initialdir=os.path.join(os.getcwd(), "saves"),
            filetypes=[("Json Documents", "*.json")],
            defaultextension=".json",
        ) as json_file:
            data = json.load(json_file)
        self.rows = list()

        for i, val in enumerate(data, 2):
            row = Row(self, i, val["servers"])
            row.update_added_servers_label()
            self.rows.append(row)

        self.infinite_loop()

    def infinite_loop(self):
        while True:
            self.update_gold_amounts()
            self.tksleep(random.randint(10, 15))


if __name__ == "__main__":
    app = App()

    def on_close():
        app.destroy()
        sys.exit()

    app.protocol("WM_DELETE_WINDOW", on_close)
    app.mainloop()
