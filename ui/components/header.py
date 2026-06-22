import customtkinter as ctk
from PIL import Image
class Header(ctk.CTkFrame):
    def __init__(self, master, comando_logout=None):
        super().__init__(master, fg_color="transparent")

        self.top_container = ctk.CTkFrame(self, fg_color="transparent")
        self.top_container.pack(fill="x", padx=40, pady=(30, 20))

        self.top_container.grid_columnconfigure(0, weight=1)
        self.top_container.grid_columnconfigure(1, weight=0)
        self.top_container.grid_columnconfigure(2, weight=1)

        self.lbl_header = ctk.CTkLabel(self.top_container, text="Sistema de Gestión de Agenda de Sesiones", font=("Arial", 26, "bold", "italic"), text_color="#006B4D")
        self.lbl_header.grid(row=0, column=1)

        try:
            ic_logout = ctk.CTkImage(light_image=Image.open("assets/ic_logout.png"), size=(25, 25))
            texto_btn = ""
        except FileNotFoundError:
            ic_logout = None
            texto_btn = "➔ Salir"

        self.btn_logout = ctk.CTkButton(self.top_container, text=texto_btn, image=ic_logout, width=40, height=40, fg_color="transparent", hover_color="#E0E0E0", text_color="black", command=comando_logout)
        self.btn_logout.grid(row=0, column=2, sticky="e")

        self.linea = ctk.CTkFrame(self, height=2, fg_color="#D3D3D3")
        self.linea.pack(fill="x", padx=40)