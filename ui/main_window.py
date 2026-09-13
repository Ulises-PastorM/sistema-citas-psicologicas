import customtkinter as ctk
from PIL import Image  
from ui.components.sidebar import Sidebar
from ui.components.header import Header
from ui.psicologa.registro_citas import RegistroCitas
from ui.psicologa.calendario import CalendarioView
from ui.psicologa.registro_usuaria import RegistroUsuariaView
from ui.login.login_view import LoginView 
from ui.psicologa.observaciones import ObservacionesView 
from ui.psicologa.mi_cuenta import MiCuentaView
import ctypes
from utils.resource_path import resource_path

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Sistema de Gestión - IMMUJER")
        self.geometry("1300x750")
        self.minsize(1300, 750)
        ctk.set_appearance_mode("light")
        self.configure(fg_color="#FDFBFB")
        self.after(10, self.bloquear_arrastre_bordes)
        self.mostrar_login()

    def bloquear_arrastre_bordes(self):
        try:
            hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
            GWL_STYLE = -16
            WS_THICKFRAME = 0x00040000 
            style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_STYLE)
            ctypes.windll.user32.SetWindowLongW(hwnd, GWL_STYLE, style & ~WS_THICKFRAME)
        except Exception as e:
            print("No se pudo aplicar el bloqueo de bordes de Windows:", e)
            
    def mostrar_login(self):
        self.login_view = LoginView(self, comando_login=self.iniciar_aplicacion)
        self.login_view.pack(fill="both", expand=True)

    def iniciar_aplicacion(self):
        self.login_view.destroy()

        self.grid_rowconfigure(0, weight=0) 
        self.grid_rowconfigure(1, weight=1) 
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        try:
            self.img_pil_banner = Image.open(resource_path("assets/banner_top.png"))
            self.img_banner = ctk.CTkImage(light_image=self.img_pil_banner, size=(1300, 20))
            
            self.lbl_banner = ctk.CTkLabel(self, image=self.img_banner, text="")
            self.lbl_banner.grid(row=0, column=0, columnspan=2, sticky="ew")
            
            self.lbl_banner.bind("<Configure>", self.redimensionar_banner)
            
        except FileNotFoundError:
            self.banner = ctk.CTkFrame(self, height=20, fg_color="#FF6B35", corner_radius=0)
            self.banner.grid(row=0, column=0, columnspan=2, sticky="ew")

        self.sidebar = Sidebar(self, comando_navegacion=self.cambiar_vista)
        self.sidebar.grid(row=1, column=0, sticky="nsew")

        self.main_container = ctk.CTkFrame(self, fg_color="#FDFBFB", corner_radius=0)
        self.main_container.grid(row=1, column=1, sticky="nsew")
        self.main_container.grid_rowconfigure(1, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

        self.header = Header(self.main_container, comando_logout=self.cerrar_sesion)
        self.header.grid(row=0, column=0, sticky="ew")

        self.vistas_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.vistas_frame.grid(row=1, column=0, sticky="nsew", padx=40, pady=(10, 30))
        self.vistas_frame.grid_rowconfigure(0, weight=1)
        self.vistas_frame.grid_columnconfigure(0, weight=1)

        self.vista_calendario = CalendarioView(self.vistas_frame)
        self.vista_registro = RegistroCitas(self.vistas_frame, on_actualizar=self.actualizar_vistas_dependientes)
        self.vista_usuaria = RegistroUsuariaView(self.vistas_frame, on_actualizar=self.actualizar_vistas_dependientes)
        self.vista_observacion = ObservacionesView(self.vistas_frame)
        self.vista_cuenta = MiCuentaView(self.vistas_frame)

        self.vista_registro.grid(row=0, column=0, sticky="nsew")
        self.vista_calendario.grid(row=0, column=0, sticky="nsew")
        self.vista_usuaria.grid(row=0, column=0, sticky="nsew")
        self.vista_observacion.grid(row=0, column=0, sticky="nsew")
        self.vista_cuenta.grid(row=0, column=0, sticky="nsew")

        self.sidebar.navegar("registro")

    def redimensionar_banner(self, event):
        nuevo_ancho = event.width
        self.img_banner.configure(size=(nuevo_ancho, 20))

    def cambiar_vista(self, nombre_vista):
        if nombre_vista == "registro":
            self.vista_registro.refrescar_usuarias()
            self.vista_registro.tkraise()
        elif nombre_vista == "calendario":
            self.vista_calendario.tkraise()
        elif nombre_vista == "usuaria":
            self.vista_usuaria.tkraise()
        elif nombre_vista == "observaciones":
            self.vista_observacion.tkraise()
        elif nombre_vista == "cuenta":            
            self.vista_cuenta.tkraise()
            
    def cerrar_sesion(self):
        for widget in self.winfo_children():
            widget.destroy()
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=1)

        self.mostrar_login()
        
    def actualizar_vistas_dependientes(self):
        if hasattr(self.vista_calendario, 'refrescar_datos'):
            self.vista_calendario.refrescar_datos()

        if hasattr(self.vista_observacion, 'refrescar_tabla'):
            self.vista_observacion.refrescar_tabla()
            
        if hasattr(self.vista_registro, 'refrescar_tabla'):
            self.vista_registro.refrescar_tabla()
            self.vista_registro.refrescar_usuarias()