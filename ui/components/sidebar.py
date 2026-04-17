import customtkinter as ctk
from PIL import Image

class Sidebar(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, width=250, corner_radius=0, fg_color="#F2F2F2")
        self.grid_rowconfigure(5, weight=1)

        ruta_logo = "assets/logo.png" 
        try:
            imagen_logo = ctk.CTkImage(light_image=Image.open(ruta_logo), size=(200, 70))
            self.lbl_logo = ctk.CTkLabel(self, image=imagen_logo, text="")
        except FileNotFoundError:
            self.lbl_logo = ctk.CTkLabel(self, text="[ IMAGEN LOGO ]", font=("Arial", 16, "bold"), text_color="#7A1B6C")
        self.lbl_logo.grid(row=0, column=0, padx=20, pady=(20, 30))

        try:
            ic_citas_n = ctk.CTkImage(light_image=Image.open("assets/ic_citas_negro.png"), size=(20, 20))
            ic_cal_n = ctk.CTkImage(light_image=Image.open("assets/ic_calendario_negro.png"), size=(20, 20))
            ic_obs_n = ctk.CTkImage(light_image=Image.open("assets/ic_observaciones_negro.png"), size=(20, 20))
            ic_usu_n = ctk.CTkImage(light_image=Image.open("assets/ic_citas_negro.png"), size=(20, 20))

            ic_citas_b = ctk.CTkImage(light_image=Image.open("assets/ic_citas_blanco.png"), size=(20, 20))
            ic_cal_b = ctk.CTkImage(light_image=Image.open("assets/ic_calendario_blanco.png"), size=(20, 20))
            ic_obs_b = ctk.CTkImage(light_image=Image.open("assets/ic_observaciones_blanco.png"), size=(20, 20))
            ic_usu_b = ctk.CTkImage(light_image=Image.open("assets/ic_citas_blanco.png"), size=(20, 20))
        except FileNotFoundError:
            ic_citas_n = ic_cal_n = ic_obs_n = ic_usu_n = None
            ic_citas_b = ic_cal_b = ic_obs_b = ic_usu_b = None

        btn_estilo = {
            "fg_color": "#E0E0E0", 
            "text_color": "black", 
            "font": ("Arial", 14, "bold", "italic"), 
            "corner_radius": 8, 
            "height": 45, 
            "hover_color": "#FF6B35", 
            "compound": "left", 
            "anchor": "w"
        }
        
        self.btn_citas = ctk.CTkButton(self, text=" Registro de Citas", image=ic_citas_n, **btn_estilo)
        self.btn_citas.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.btn_calendario = ctk.CTkButton(self, text=" Calendario", image=ic_cal_n, **btn_estilo)
        self.btn_calendario.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.btn_observaciones = ctk.CTkButton(self, text=" Observaciones", image=ic_obs_n, **btn_estilo)
        self.btn_observaciones.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        self.btn_usuaria = ctk.CTkButton(self, text=" Registro de Usuaria", image=ic_usu_n, **btn_estilo)
        self.btn_usuaria.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

        self.aplicar_efecto_hover(self.btn_citas, ic_citas_n, ic_citas_b)
        self.aplicar_efecto_hover(self.btn_calendario, ic_cal_n, ic_cal_b)
        self.aplicar_efecto_hover(self.btn_observaciones, ic_obs_n, ic_obs_b)
        self.aplicar_efecto_hover(self.btn_usuaria, ic_usu_n, ic_usu_b)

    def aplicar_efecto_hover(self, boton, icono_negro, icono_blanco):
        def on_enter(event):
            boton.configure(text_color="white", image=icono_blanco, fg_color="#FF6B35")
            
        def on_leave(event):
            boton.configure(text_color="black", image=icono_negro, fg_color="#E0E0E0")
            
        boton.bind("<Enter>", on_enter)
        boton.bind("<Leave>", on_leave)