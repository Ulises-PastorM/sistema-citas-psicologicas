import customtkinter as ctk
from PIL import Image
from services.usuarios_sistema_services import service_login

class LoginView(ctk.CTkFrame):
    def __init__(self, master, comando_login):
        super().__init__(master, fg_color="#F8E8E8") 
        self.comando_login = comando_login

        self.card = ctk.CTkFrame(self, fg_color="white", corner_radius=20, width=450, height=520)
        self.card.place(relx=0.5, rely=0.5, anchor="center")
        self.card.pack_propagate(False)

        try:
            img_logo = ctk.CTkImage(light_image=Image.open("assets/logo.png"), size=(200, 70))
            lbl_logo = ctk.CTkLabel(self.card, image=img_logo, text="")
        except FileNotFoundError:
            lbl_logo = ctk.CTkLabel(self.card, text="[ IMAGEN LOGO ]", font=("Arial", 20, "bold"), text_color="#7A1B6C")
        lbl_logo.pack(pady=(25, 10))

        ctk.CTkLabel(self.card, text="Sistema de Gestión de Agenda de Sesiones", font=("Arial", 16, "bold", "italic"), text_color="#006B4D").pack(pady=(0, 20))

        sub_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        sub_frame.pack(fill="x", padx=40, pady=(0, 20))
        
        sub_frame.grid_columnconfigure(0, weight=1)
        sub_frame.grid_columnconfigure(1, weight=0)
        sub_frame.grid_columnconfigure(2, weight=1)
        
        ctk.CTkFrame(sub_frame, height=2, fg_color="#E0E0E0").grid(row=0, column=0, sticky="ew", padx=(0, 15))
        ctk.CTkLabel(sub_frame, text="Iniciar Sesión", font=("Arial", 18, "bold", "italic"), text_color="#7A1B6C").grid(row=0, column=1)
        ctk.CTkFrame(sub_frame, height=2, fg_color="#E0E0E0").grid(row=0, column=2, sticky="ew", padx=(15, 0))
        
        frame_user = ctk.CTkFrame(self.card, fg_color="white", border_width=2, border_color="#E8E8E8", corner_radius=20, height=45)
        frame_user.pack(fill="x", padx=60, pady=(0, 15))
        frame_user.pack_propagate(False) 
        
        try:
            ic_user = ctk.CTkImage(light_image=Image.open("assets/ic_user.png"), size=(20, 20))
            ctk.CTkLabel(frame_user, image=ic_user, text="").pack(side="left", padx=(15, 5))
        except FileNotFoundError:
            ctk.CTkLabel(frame_user, text="👤", text_color="gray").pack(side="left", padx=(15, 5))
            
        self.ent_usuario = ctk.CTkEntry(frame_user, placeholder_text="Usuario", fg_color="white", border_width=0, text_color="black")
        self.ent_usuario.pack(side="left", fill="both", expand=True, padx=(0, 15), pady=2)

        frame_pwd = ctk.CTkFrame(self.card, fg_color="white", border_width=2, border_color="#E8E8E8", corner_radius=20, height=45)
        frame_pwd.pack(fill="x", padx=60, pady=(0, 0))
        frame_pwd.pack_propagate(False)
        
        try:
            ic_lock = ctk.CTkImage(light_image=Image.open("assets/ic_lock.png"), size=(20, 20))
            ctk.CTkLabel(frame_pwd, image=ic_lock, text="").pack(side="left", padx=(15, 5))
        except FileNotFoundError:
            ctk.CTkLabel(frame_pwd, text="🔒", text_color="gray").pack(side="left", padx=(15, 5))
            
        self.ent_password = ctk.CTkEntry(frame_pwd, placeholder_text="Contraseña", show="*", fg_color="white", border_width=0, text_color="black")
        self.ent_password.pack(side="left", fill="both", expand=True, padx=(0, 15), pady=2)
        
        self.lbl_error = ctk.CTkLabel(self.card, text="", text_color="red", font=("Arial", 12, "bold"))
        self.lbl_error.pack(pady=(2, 5))
        
        self.btn_login = ctk.CTkButton(self.card, text="Iniciar Sesión", fg_color="#FF6B35", hover_color="#E55A2B", text_color="white", font=("Arial", 16, "bold"), corner_radius=20, height=45, command=self.validar_login)
        self.btn_login.pack(fill="x", padx=60, pady=(0, 5))

        #ctk.CTkLabel(self.card, text="¿Olvidaste tu contraseña?", font=("Arial", 12, "bold", "italic"), text_color="#7A1B6C", cursor="hand2").pack(pady=(5, 0))

        try:
            img_wave = ctk.CTkImage(light_image=Image.open("assets/banner_buttom.png"), size=(450, 80))
            lbl_wave = ctk.CTkLabel(self.card, image=img_wave, text="")
            lbl_wave.place(relx=0.5, rely=1.0, anchor="s")
        except FileNotFoundError:
            ctk.CTkFrame(self.card, fg_color="#7A1B6C", height=30, corner_radius=20).place(relx=0.5, rely=1.0, anchor="s", relwidth=1.0)

    def validar_login(self):
        user = self.ent_usuario.get()
        pwd = self.ent_password.get()
        
        if not user or not pwd:
            self.lbl_error.configure(text="Por favor, completa todos los campos.")
            return
        
        respuesta = service_login(user, pwd)
        
        if respuesta.get("success"):
            self.lbl_error.configure(text="") 
            self.comando_login() 
        else:
            error_msg = respuesta.get("error", "Usuario o contraseña incorrectos")
            self.lbl_error.configure(text=error_msg)