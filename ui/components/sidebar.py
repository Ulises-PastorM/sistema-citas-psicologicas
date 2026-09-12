import customtkinter as ctk
from PIL import Image
from utils.resource_path import resource_path
class Sidebar(ctk.CTkFrame):
    def __init__(self, master, comando_navegacion=None):
        super().__init__(master, width=250, corner_radius=0, fg_color="#F2F2F2")
        self.grid_rowconfigure(5, weight=1)
        self.comando_navegacion = comando_navegacion
        self.vista_actual = None 

        ruta_logo = resource_path("assets/logo.png")
        try:
            imagen_logo = ctk.CTkImage(light_image=Image.open(resource_path(ruta_logo)), size=(200, 70))
            self.lbl_logo = ctk.CTkLabel(self, image=imagen_logo, text="")
        except FileNotFoundError:
            self.lbl_logo = ctk.CTkLabel(self, text="[ IMAGEN LOGO ]", font=("Arial", 17, "bold"), text_color="#7A1B6C")
        self.lbl_logo.grid(row=0, column=0, padx=20, pady=(20, 30))

        self.iconos_n = {}
        self.iconos_b = {}
        try:
            self.iconos_n["registro"] = ctk.CTkImage(light_image=Image.open(resource_path("assets/ic_citas_negro.png")), size=(20, 20))
            self.iconos_n["usuaria"] = ctk.CTkImage(light_image=Image.open(resource_path("assets/ic_citas_negro.png")), size=(20, 20))
            self.iconos_n["calendario"] = ctk.CTkImage(light_image=Image.open(resource_path("assets/ic_calendario_negro.png")), size=(20, 20))
            self.iconos_n["observaciones"] = ctk.CTkImage(light_image=Image.open(resource_path("assets/ic_observaciones_negro.png")), size=(20, 20))

            self.iconos_b["registro"] = ctk.CTkImage(light_image=Image.open(resource_path("assets/ic_citas_blanco.png")), size=(20, 20))
            self.iconos_b["usuaria"] = ctk.CTkImage(light_image=Image.open(resource_path("assets/ic_citas_blanco.png")), size=(20, 20))
            self.iconos_b["calendario"] = ctk.CTkImage(light_image=Image.open(resource_path("assets/ic_calendario_blanco.png")), size=(20, 20))
            self.iconos_b["observaciones"] = ctk.CTkImage(light_image=Image.open(resource_path("assets/ic_observaciones_blanco.png")), size=(20, 20))

        except FileNotFoundError:
            for k in ["registro","usuaria", "calendario", "observaciones"]:
                self.iconos_n[k] = self.iconos_b[k] = None

        btn_estilo = {
            "fg_color": "#E0E0E0", "text_color": "black", "font": ("Arial", 15, "bold", "italic"),
            "corner_radius": 8, "height": 45, "compound": "left", "anchor": "w"
        }
        
        # Botones
        self.btn_citas = ctk.CTkButton(self, text=" Registro de Citas", image=self.iconos_n["registro"], **btn_estilo, command=lambda: self.navegar("registro"))
        self.btn_citas.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        self.btn_usuaria = ctk.CTkButton(self, text=" Registro de Usuaria", image=self.iconos_n["usuaria"], **btn_estilo, command=lambda: self.navegar("usuaria"))
        self.btn_usuaria.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.btn_calendario = ctk.CTkButton(self, text=" Calendario", image=self.iconos_n["calendario"], **btn_estilo, command=lambda: self.navegar("calendario"))
        self.btn_calendario.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        self.btn_observaciones = ctk.CTkButton(self, text=" Observaciones", image=self.iconos_n["observaciones"], **btn_estilo, command=lambda: self.navegar("observaciones"))
        self.btn_observaciones.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

        # Diccionario de botones para iterar fácilmente
        self.botones = {
            "registro": self.btn_citas,
            "usuaria": self.btn_usuaria,
            "calendario": self.btn_calendario,
            "observaciones": self.btn_observaciones
        }

        for nombre, btn in self.botones.items():
            self.aplicar_efecto_hover(btn, nombre)
            
        self.separador = ctk.CTkFrame(self, height=1, fg_color="#D3D3D3")
        self.separador.grid(row=6, column=0, padx=20, pady=(0, 15), sticky="ew")

        icono_cuenta = ctk.CTkImage(light_image=Image.open(resource_path("assets/ic_userP.png")), size=(20, 20))

        self.btn_cuenta = ctk.CTkButton(
            self,
            text=" Ver mi Cuenta      >", 
            image=icono_cuenta,              
            compound="left",                 
            fg_color="transparent",
            text_color="#FF6B35",
            border_color="#FF6B35",
            border_width=1,
            hover_color="#FFF0EB",
            font=("Arial", 15, "bold"),
            corner_radius=8,
            height=40,
            command=lambda: self.navegar("cuenta") 
        )
        self.btn_cuenta.grid(row=7, column=0, padx=20, pady=(0, 15), sticky="ew")
            
        self.btn_creditos = ctk.CTkButton(
            self, 
            text="Acerca del Sistema", 
            fg_color="transparent", 
            text_color="#7A1B6C", 
            font=("Arial", 13, "underline"), 
            hover_color="#D3D3D3", 
            command=self.mostrar_creditos
        )
        self.btn_creditos.grid(row=8, column=0, padx=20, pady=(0, 20), sticky="s")

    def navegar(self, vista_nombre):
        self.set_active(vista_nombre) 
        if self.comando_navegacion:
            self.comando_navegacion(vista_nombre) 

    def set_active(self, vista_nombre):
        self.vista_actual = vista_nombre
        for nombre, btn in self.botones.items():
            if nombre == vista_nombre:
                btn.configure(fg_color="#FF6B35", text_color="white", image=self.iconos_b[nombre])
            else:
                btn.configure(fg_color="#E0E0E0", text_color="black", image=self.iconos_n[nombre])

    def aplicar_efecto_hover(self, boton, nombre):
        def on_enter(event):
            if self.vista_actual != nombre:
                boton.configure(text_color="white", image=self.iconos_b[nombre], fg_color="#FF6B35")
        def on_leave(event):
            if self.vista_actual != nombre:
                boton.configure(text_color="black", image=self.iconos_n[nombre], fg_color="#E0E0E0")
                
        boton.bind("<Enter>", on_enter)
        boton.bind("<Leave>", on_leave)
        
    def mostrar_creditos(self):
        modal = ctk.CTkToplevel(self)
        modal.title("Acerca del Sistema")
        modal.geometry("450x340")
        modal.resizable(False, False)
        modal.transient(self.winfo_toplevel())
        modal.grab_set()

        ctk.CTkLabel(modal, text="Sistema de Gestión - IMMUJER", font=("Arial", 17, "bold"), text_color="#7A1B6C").pack(pady=(20, 10))

        info_texto = (
            "Este sistema fue desarrollado como proyecto\n"
            "de Servicio Social por estudiantes de Ingeniería en Computación\n"
            "de la Universidad Tecnológica de la Mixteca.\n\n"
            "Desarrolladores:\n"
            "  Leonardo Roque Hernández\n"
            "  Contacto: leonardoroque711@gmail.com\n"
            "  Ulises Pastor Martínez\n"
            "  Contacto: pmudev14@gmail.com\n\n"
            "Desarrollado para:\n"
            "INSTANCIA MUNICIPAL DE LA MUJER."
        )

        ctk.CTkLabel(modal, text=info_texto, font=("Arial", 14), justify="center").pack(pady=10)

        ctk.CTkButton(modal, text="Cerrar", command=modal.destroy, fg_color="#FF6B35", text_color="white").pack(pady=(10, 20))