import customtkinter as ctk

class RegistroCitas(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Título
        self.lbl_titulo = ctk.CTkLabel(self, text="Registro de Citas para Atención Psicológica", font=("Arial", 20, "bold", "italic"), text_color="#006B4D")
        self.lbl_titulo.grid(row=0, column=0, pady=(0, 10), sticky="w")

        self.card_frame = ctk.CTkFrame(self, fg_color="#F4F4F4", corner_radius=15)
        self.card_frame.grid(row=1, column=0, sticky="nsew")
        self.card_frame.grid_columnconfigure((0, 1), weight=1)

        #SECCIÓN TABLA
        self.lbl_subtitulo1 = ctk.CTkLabel(self.card_frame, text="Registro de Citas", font=("Arial", 16, "bold", "italic"), text_color="#006B4D")
        self.lbl_subtitulo1.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 10), sticky="w")

        self.tabla_header = ctk.CTkFrame(self.card_frame, fg_color="#7A1B6C", corner_radius=8, height=40)
        self.tabla_header.grid(row=1, column=0, columnspan=2, padx=20, pady=5, sticky="ew")
        
        columnas = ["Nombre", "Edad", "Fecha", "Telefono", "Estatus", "Editar"]
        self.tabla_header.grid_columnconfigure(list(range(6)), weight=1)
        for i, col in enumerate(columnas):
            lbl = ctk.CTkLabel(self.tabla_header, text=col, text_color="white", font=("Arial", 13, "bold"))
            lbl.grid(row=0, column=i, pady=10)

        #FORMULARIO
        self.lbl_subtitulo2 = ctk.CTkLabel(self.card_frame, text="Registrar Nueva Cita", font=("Arial", 16, "bold", "italic"), text_color="#006B4D")
        self.lbl_subtitulo2.grid(row=2, column=0, columnspan=2, padx=20, pady=(30, 10), sticky="w")

        entry_kwargs = {"fg_color": "white", "text_color": "black", "border_width": 1, "border_color": "#D3D3D3", "corner_radius": 15, "height": 40}

        self.ent_nombre = ctk.CTkEntry(self.card_frame, placeholder_text="Nombre:", **entry_kwargs)
        self.ent_nombre.grid(row=3, column=0, padx=(20, 10), pady=10, sticky="ew")

        self.ent_colonia = ctk.CTkEntry(self.card_frame, placeholder_text="Colonia:", **entry_kwargs)
        self.ent_colonia.grid(row=3, column=1, padx=(10, 20), pady=10, sticky="ew")

        self.ent_fecha = ctk.CTkEntry(self.card_frame, placeholder_text="Fecha:", **entry_kwargs)
        self.ent_fecha.grid(row=4, column=0, padx=(20, 10), pady=10, sticky="ew")

        self.ent_telefono = ctk.CTkEntry(self.card_frame, placeholder_text="Telefono:", **entry_kwargs)
        self.ent_telefono.grid(row=4, column=1, padx=(10, 20), pady=10, sticky="ew")

        self.ent_horario = ctk.CTkEntry(self.card_frame, placeholder_text="Horario:", **entry_kwargs)
        self.ent_horario.grid(row=5, column=0, padx=(20, 10), pady=10, sticky="ew")

        self.btn_registrar = ctk.CTkButton(self.card_frame, text="+ Registrar Nuevo", fg_color="#FF6B35", text_color="white", font=("Arial", 15, "bold"), corner_radius=8, height=45)
        self.btn_registrar.grid(row=6, column=1, padx=20, pady=(20, 30), sticky="e")