import customtkinter as ctk

class ObservacionesView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.lbl_titulo = ctk.CTkLabel(self, text="Observaciones de la Sesión", font=("Arial", 22, "bold", "italic"), text_color="#006B4D")
        self.lbl_titulo.grid(row=0, column=0, pady=(0, 5), sticky="w")

        self.linea = ctk.CTkFrame(self, height=1, fg_color="#D3D3D3")
        self.linea.grid(row=1, column=0, sticky="ew", pady=(0, 15))

        self.card_frame = ctk.CTkFrame(self, fg_color="#F4F4F4", corner_radius=15)
        self.card_frame.grid(row=2, column=0, sticky="nsew")
        self.card_frame.grid_columnconfigure(0, weight=1)
        self.card_frame.grid_rowconfigure(2, weight=1)

        self.lbl_subtitulo = ctk.CTkLabel(self.card_frame, text="Registro de Sesiones", font=("Arial", 16, "bold", "italic"), text_color="#006B4D")
        self.lbl_subtitulo.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        self.tabla_header = ctk.CTkFrame(self.card_frame, fg_color="#7A1B6C", corner_radius=8, height=40)
        self.tabla_header.grid(row=1, column=0, padx=(20, 35), pady=(0, 5), sticky="ew")
        self.tabla_header.grid_columnconfigure(list(range(6)), weight=1, uniform="col")
        self.tabla_header.pack_propagate(False)
        
        columnas = ["Nombre", "Edad", "Fecha", "Telefono", "Estatus", "Editar"]
        for i, col in enumerate(columnas):
            lbl = ctk.CTkLabel(self.tabla_header, text=col, text_color="white", font=("Arial", 13, "bold"), anchor="center")
            lbl.grid(row=0, column=i, pady=10, sticky="ew")

        self.scroll_tabla = ctk.CTkScrollableFrame(self.card_frame, fg_color="transparent")
        self.scroll_tabla.grid(row=2, column=0, padx=15, pady=(0, 20), sticky="nsew")

        datos_ejemplo = [
            ("Ana Martinez", "28", "09/Mar/2026", "5550101999", "Activa"),
            ("Maria Lopez", "34", "15/Abr/2026", "5550202888", "Pendiente"),
            ("Juana Perez", "42", "20/May/2026", "5550303777", "Completada"),
            ("Laura Gomez", "25", "22/May/2026", "5550404666", "Activa"),
        ]

        for fila in datos_ejemplo:
            row_frame = ctk.CTkFrame(self.scroll_tabla, fg_color="white", border_width=1, border_color="#E0E0E0", corner_radius=6, height=40)
            row_frame.pack(fill="x", pady=3, padx=5)
            row_frame.grid_columnconfigure(list(range(6)), weight=1, uniform="col")
            row_frame.grid_propagate(False)

            for i in range(5):
                color_texto = "#32CD32" if fila[4] == "Activa" and i == 4 else "black"
                lbl_dato = ctk.CTkLabel(row_frame, text=fila[i], text_color=color_texto, font=("Arial", 12), anchor="center")
                lbl_dato.grid(row=0, column=i, pady=8, sticky="ew")
            
            btn_editar = ctk.CTkButton(row_frame, text="Editar Observaciones", width=30, height=24, fg_color="#7A1B6C", hover_color="#E55B2B", text_color="white", corner_radius=5, command=lambda n=fila[0]: self.abrir_modal(n))
            btn_editar.grid(row=0, column=5, pady=8)
            
    def abrir_modal(self, nombre_usuaria):
        modal = ctk.CTkToplevel(self)
        modal.geometry("450x300")
        
        modal.overrideredirect(True) 
        modal.attributes("-topmost", True)
        modal.configure(fg_color="#D3D3D3") 
        
        modal.update_idletasks()
        x = self.winfo_rootx() + (self.winfo_width() // 2) - (450 // 2)
        y = self.winfo_rooty() + (self.winfo_height() // 2) - (300 // 2)
        modal.geometry(f"+{x}+{y}")

        container = ctk.CTkFrame(modal, fg_color="white", corner_radius=10, border_width=1, border_color="#A0A0A0")
        container.pack(fill="both", expand=True)

        header = ctk.CTkFrame(container, fg_color="#FF6B35", corner_radius=8, height=45)
        header.pack(fill="x", padx=1, pady=1)
        header.pack_propagate(False)

        lbl_modal_title = ctk.CTkLabel(header, text="Agregar observaciones", font=("Arial", 16, "bold", "italic"), text_color="white")
        lbl_modal_title.pack(side="left", padx=15)

        btn_close = ctk.CTkButton(header, text="X", font=("Arial", 18, "bold"), text_color="white", fg_color="transparent", hover_color="#E55A2B", width=30, command=modal.destroy)
        btn_close.pack(side="right", padx=10)

        content = ctk.CTkFrame(container, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=25, pady=15)

        ctk.CTkLabel(content, text=nombre_usuaria, font=("Arial", 16, "bold", "italic"), text_color="black").pack(anchor="w")
        ctk.CTkLabel(content, text="Observaciones de la sesión", font=("Arial", 11, "bold", "italic"), text_color="black").pack(anchor="w", pady=(0, 5))

        self.txt_obs = ctk.CTkTextbox(content, fg_color="white", text_color="black", border_width=1, border_color="#D3D3D3", height=100)
        self.txt_obs.pack(fill="x", pady=(0, 15))

        footer_frame = ctk.CTkFrame(content, fg_color="transparent")
        footer_frame.pack(fill="x", pady=(5, 0))

        lbl_mensaje = ctk.CTkLabel(footer_frame, text="", font=("Arial", 12, "bold"))
        lbl_mensaje.pack(side="left")

        def guardar_observaciones():
            lbl_mensaje.configure(text="✅ Datos modificados exitosamente", text_color="#32CD32")
            
            btn_guardar.configure(state="disabled")
            
            self.after(1500, modal.destroy)

        btn_guardar = ctk.CTkButton(footer_frame, text="Guardar", fg_color="#005A43", hover_color="#004030", text_color="white", font=("Arial", 14, "bold", "italic"), corner_radius=8, height=35, command=guardar_observaciones)
        btn_guardar.pack(side="right")
        