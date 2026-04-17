import customtkinter as ctk
from PIL import Image  
from ui.components.sidebar import Sidebar
from ui.components.header import Header
from ui.psicologa.registro_citas import RegistroCitas

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Sistema de Gestión - IMMUJER")
        self.geometry("1100x750")
        self.minsize(1100, 750)
        ctk.set_appearance_mode("light")

        self.grid_rowconfigure(0, weight=0) 
        self.grid_rowconfigure(1, weight=1) 
        self.grid_columnconfigure(1, weight=1)

        try:
            img_banner = ctk.CTkImage(light_image=Image.open("assets/banner_top.png"), size=(1100, 20))
            self.lbl_banner = ctk.CTkLabel(self, image=img_banner, text="")
            self.lbl_banner.grid(row=0, column=0, columnspan=2, sticky="ew")
        except FileNotFoundError:
            self.banner = ctk.CTkFrame(self, height=20, fg_color="#FF6B35", corner_radius=0)
            self.banner.grid(row=0, column=0, columnspan=2, sticky="ew")

        self.sidebar = Sidebar(self)
        self.sidebar.grid(row=1, column=0, sticky="nsew")

        self.main_container = ctk.CTkFrame(self, fg_color="#FDFBFB", corner_radius=0)
        self.main_container.grid(row=1, column=1, sticky="nsew")
        self.main_container.grid_rowconfigure(1, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

        self.header = Header(self.main_container)
        self.header.grid(row=0, column=0, sticky="ew")

        self.registro_citas = RegistroCitas(self.main_container)
        self.registro_citas.grid(row=1, column=0, sticky="nsew", padx=40, pady=(10, 30))