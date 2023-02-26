import customtkinter
from PIL import Image
import os


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        image_path = os.path.join(os.getcwd(), "icons")
        self.set_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "submit.png"))
        )
        self.title("FunPay")
        self.geometry("300x100")
        self.resizable(True, True)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.title_label = customtkinter.CTkLabel(
            self,
            corner_radius=0,
            height=40,
            font=customtkinter.CTkFont(size=30),
            text=f"Set password",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
        )
        self.title_label.grid(row=0, column=0, sticky="ew")
        self.password_entry = customtkinter.CTkEntry(
            self,
            placeholder_text="Set Password:",
            corner_radius=0,
            font=customtkinter.CTkFont(size=15),
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            height=28,
            border_width=1,
        )
        self.password_entry.grid(row=1, column=0, sticky="ew", padx=5)
        self.set_button = customtkinter.CTkButton(
            self,
            corner_radius=0,
            height=20,
            width=10,
            font=customtkinter.CTkFont(size=15),
            text="Set",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            command=self.set_button_on_click,
            image=self.set_image,
        )
        self.set_button.grid(row=1, column=1, sticky="ew", padx=5)

    def set_button_on_click(self):
        ...


if __name__ == "__main__":
    app = App()
    app.mainloop()
