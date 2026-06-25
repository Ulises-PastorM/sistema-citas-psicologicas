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

        self.btn_logout = ctk.CTkButton(
            self.top_container, 
            text="Cerrar sesión", 
            font=("Arial", 14, "bold", "italic"),
            width=140, 
            height=45, 
            corner_radius=8, 
            fg_color="#E0E0E0",
            text_color="black",
            command=comando_logout
        )
        self.btn_logout.grid(row=0, column=2, sticky="e")

        def on_enter(event):
            self.btn_logout.configure(fg_color="#FF6B35", text_color="white")

        def on_leave(event):
            self.btn_logout.configure(fg_color="#E0E0E0", text_color="black")

        self.btn_logout.bind("<Enter>", on_enter)
        self.btn_logout.bind("<Leave>", on_leave)

        self.linea = ctk.CTkFrame(self, height=2, fg_color="#D3D3D3")
        self.linea.pack(fill="x", padx=40)