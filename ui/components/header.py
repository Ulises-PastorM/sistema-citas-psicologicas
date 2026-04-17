import customtkinter as ctk

class Header(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        
        self.lbl_header = ctk.CTkLabel(self, text="Sistema de Gestión de Agenda de Sesiones",font=("Arial", 26, "bold", "italic"), text_color="#006B4D")
        self.lbl_header.pack(pady=(30, 20))

        self.linea = ctk.CTkFrame(self, height=2, fg_color="#D3D3D3")
        self.linea.pack(fill="x", padx=40)