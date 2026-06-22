import customtkinter as ctk

class RegistroCitas(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.lbl_titulo = ctk.CTkLabel(self, text="Registro de Citas para Atención Psicológica", font=("Arial", 20, "bold", "italic"), text_color="#006B4D")
        self.lbl_titulo.grid(row=0, column=0, pady=(0, 10), sticky="w")

        self.card_frame = ctk.CTkScrollableFrame(self, fg_color="#F4F4F4", corner_radius=15)
        self.card_frame.grid(row=1, column=0, sticky="nsew")
        self.card_frame.grid_columnconfigure((0, 1), weight=1)

        self.lbl_subtitulo1 = ctk.CTkLabel(self.card_frame, text="Registro de Citas", font=("Arial", 16, "bold", "italic"), text_color="#006B4D")
        self.lbl_subtitulo1.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 10), sticky="w")

        self.tabla_header = ctk.CTkFrame(self.card_frame, fg_color="#7A1B6C", corner_radius=8, height=40)
        self.tabla_header.grid(row=1, column=0, columnspan=2, padx=(20, 35), pady=(0, 5), sticky="ew")
        self.tabla_header.grid_columnconfigure(list(range(6)), weight=1, uniform="col")
        self.tabla_header.pack_propagate(False)
        
        columnas = ["Nombre", "Edad", "Fecha", "Telefono", "Estatus", "Editar"]
        for i, col in enumerate(columnas):
            lbl = ctk.CTkLabel(self.tabla_header, text=col, text_color="white", font=("Arial", 13, "bold"), anchor="center")
            lbl.grid(row=0, column=i, pady=10, sticky="ew")

        self.scroll_tabla = ctk.CTkScrollableFrame(self.card_frame, fg_color="transparent", height=160)
        self.scroll_tabla.grid(row=2, column=0, columnspan=2, padx=15, pady=(0, 10), sticky="ew")

        datos_ejemplo = [
            ("Ana Martinez", "28", "09/Mar/2026", "5550101999", "Activa"),
            ("Maria Lopez", "34", "15/Abr/2026", "5550202888", "Pendiente"),
            ("Juana Perez", "42", "20/May/2026", "5550303777", "Completada"),
            ("Laura Gomez", "25", "22/May/2026", "5550404666", "Activa"),
            ("Carmen Ruiz", "50", "01/Jun/2026", "5550505555", "Pendiente"),
            ("Rosa Sanchez", "31", "10/Jun/2026", "5550606444", "Activa")
        ]

        # Llenado de la tabla
        for fila in datos_ejemplo:
            row_frame = ctk.CTkFrame(self.scroll_tabla, fg_color="white", border_width=1, border_color="#E0E0E0", corner_radius=6, height=40)
            row_frame.pack(fill="x", pady=3, padx=5)
            row_frame.grid_columnconfigure(list(range(6)), weight=1, uniform="col")
            row_frame.grid_propagate(False)

            for i in range(5):
                color_texto = "#32CD32" if fila[4] == "Activa" and i == 4 else "black"
                lbl_dato = ctk.CTkLabel(row_frame, text=fila[i], text_color=color_texto, font=("Arial", 12), anchor="center")
                lbl_dato.grid(row=0, column=i, pady=8, sticky="ew")
            
            # AGREGAMOS EL COMMAND AL BOTÓN EDITAR
            # Usamos lambda f=fila para asegurarnos de pasar los datos correctos de esta fila en específico
            btn_editar = ctk.CTkButton(row_frame, text="Editar ✏️", width=30, height=24, fg_color="#7A1B6C", hover_color="#E55B2B", text_color="white", corner_radius=5, 
                                       command=lambda f=fila: self.abrir_modal_editar(f))
            btn_editar.grid(row=0, column=5, pady=8)

        self.lbl_subtitulo2 = ctk.CTkLabel(self.card_frame, text="Registrar Nueva Cita", font=("Arial", 16, "bold", "italic"), text_color="#006B4D")
        self.lbl_subtitulo2.grid(row=3, column=0, columnspan=2, padx=20, pady=(20, 10), sticky="w")

        lbl_kwargs = {"font": ("Arial", 12, "bold"), "text_color": "#4A4A4A"}
        opt_kwargs = {"fg_color": "white", "text_color": "black", "button_color": "#E6E6E6", "button_hover_color": "#D3D3D3", 
                      "dropdown_fg_color": "white", "dropdown_text_color": "black", "dropdown_hover_color": "#F0F0F0", 
                      "corner_radius": 6, "height": 38}

        ctk.CTkLabel(self.card_frame, text="Seleccionar Usuaria:", **lbl_kwargs).grid(row=4, column=0, padx=(20, 10), pady=(10, 0), sticky="w")
        
        lista_usuarias = ["Seleccionar...", "Ana Martinez", "Maria Lopez", "Juana Perez", "Laura Gomez"]
        self.opt_usuaria = ctk.CTkOptionMenu(self.card_frame, values=lista_usuarias, **opt_kwargs)
        self.opt_usuaria.grid(row=5, column=0, padx=(20, 10), pady=(2, 10), sticky="ew")

        ctk.CTkLabel(self.card_frame, text="Fecha 📅:", **lbl_kwargs).grid(row=4, column=1, padx=(10, 20), pady=(10, 0), sticky="w")
        
        self.frame_fecha = ctk.CTkFrame(self.card_frame, fg_color="transparent")
        self.frame_fecha.grid(row=5, column=1, padx=(10, 20), pady=(2, 10), sticky="w")

        self.opt_dia = ctk.CTkOptionMenu(self.frame_fecha, values=[str(i).zfill(2) for i in range(1, 32)], width=75, **opt_kwargs)
        self.opt_dia.set("Día")
        self.opt_dia.pack(side="left", padx=(0, 5))

        self.opt_mes = ctk.CTkOptionMenu(self.frame_fecha, values=["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"], width=110, **opt_kwargs)
        self.opt_mes.set("Mes")
        self.opt_mes.pack(side="left", padx=5)

        self.opt_ano = ctk.CTkOptionMenu(self.frame_fecha, values=["2026", "2027", "2028"], width=85, **opt_kwargs)
        self.opt_ano.set("Año")
        self.opt_ano.pack(side="left", padx=(5, 0))

        ctk.CTkLabel(self.card_frame, text="Horario 🕒:", **lbl_kwargs).grid(row=6, column=0, padx=(20, 10), pady=(10, 0), sticky="w")
        
        self.frame_horario = ctk.CTkFrame(self.card_frame, fg_color="transparent")
        self.frame_horario.grid(row=7, column=0, padx=(20, 10), pady=(2, 10), sticky="w")

        self.opt_hora = ctk.CTkOptionMenu(self.frame_horario, values=[str(i).zfill(2) for i in range(1, 21)], width=85, **opt_kwargs)
        self.opt_hora.set("Hora")
        self.opt_hora.pack(side="left", padx=(0, 5))

        ctk.CTkLabel(self.frame_horario, text=":", font=("Arial", 16, "bold"), text_color="black").pack(side="left")

        self.opt_minuto = ctk.CTkOptionMenu(self.frame_horario, values=["00", "15", "30", "45"], width=85, **opt_kwargs)
        self.opt_minuto.set("Min.")
        self.opt_minuto.pack(side="left", padx=(5, 0))

        self.btn_registrar = ctk.CTkButton(self.card_frame, text="+ Registrar Cita", fg_color="#FF6B35", text_color="white", font=("Arial", 14, "bold"), corner_radius=8, height=40)
        self.btn_registrar.grid(row=7, column=1, padx=20, pady=(10, 30), sticky="e")

    def abrir_modal_editar(self, datos_fila):
        nombre, edad, fecha, telefono, estatus = datos_fila

        modal = ctk.CTkToplevel(self)
        modal.title("Editar Cita")
        modal.geometry("400x520")
        modal.resizable(False, False)
        
        modal.transient(self.winfo_toplevel())
        modal.grab_set()

        ctk.CTkLabel(modal, text="Editar Cita", font=("Arial", 24, "bold"), text_color="#7A1B6C").pack(pady=(20, 15))

        entry_style = {"fg_color": "white", "text_color": "black", "border_width": 1, "border_color": "#D3D3D3", "corner_radius": 6, "height": 35}

        def crear_input_modal(texto, valor_inicial):
            ctk.CTkLabel(modal, text=texto, font=("Arial", 12, "bold"), text_color="#555555").pack(anchor="w", padx=40)
            ent = ctk.CTkEntry(modal, **entry_style)
            ent.insert(0, valor_inicial) 
            ent.pack(fill="x", padx=40, pady=(0, 10))
            return ent

        ent_nombre = crear_input_modal("Nombre:", nombre)
        ent_edad = crear_input_modal("Edad:", edad)
        ent_fecha = crear_input_modal("Fecha:", fecha)
        ent_telefono = crear_input_modal("Teléfono:", telefono)


        ctk.CTkLabel(modal, text="Estatus:", font=("Arial", 12, "bold"), text_color="#555555").pack(anchor="w", padx=40)
        opt_estatus = ctk.CTkOptionMenu(modal, values=["Activa", "Pendiente", "Completada", "Cancelada"], fg_color="white", text_color="black", button_color="#E6E6E6", button_hover_color="#D3D3D3", dropdown_fg_color="white", dropdown_text_color="black", corner_radius=6, height=35)
        opt_estatus.set(estatus) 
        opt_estatus.pack(fill="x", padx=40, pady=(0, 10))

        lbl_mensaje = ctk.CTkLabel(modal, text="", font=("Arial", 12, "bold"))
        lbl_mensaje.pack(pady=(5, 0))

        def guardar_modificacion():

            lbl_mensaje.configure(text="✅ Datos modificados exitosamente", text_color="#32CD32")
            
            self.after(1500, modal.destroy)

        btn_guardar = ctk.CTkButton(modal, text="Aceptar modificación", command=guardar_modificacion, fg_color="#FF6B35", hover_color="#E55B2B", text_color="white", font=("Arial", 14, "bold"), corner_radius=8, height=40)
        btn_guardar.pack(pady=(10, 20))