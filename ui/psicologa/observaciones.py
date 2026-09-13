import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox
from services.citas_services import service_obtener_citas_usuarias
from models.sesion_model import Sesion
from services.sesiones_services import (
    service_obtener_sesiones_por_cita,
    service_crear_sesion,
    service_actualizar_sesion
)

class ObservacionesView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#FDFBFB")
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.lbl_titulo = ctk.CTkLabel(self, text="Observaciones de la Sesión", font=("Arial", 23, "bold", "italic"), text_color="#006B4D")
        self.lbl_titulo.grid(row=0, column=0, pady=(0, 5), sticky="w")

        self.linea = ctk.CTkFrame(self, height=1, fg_color="#D3D3D3")
        self.linea.grid(row=1, column=0, sticky="ew", pady=(0, 15))

        self.card_frame = ctk.CTkFrame(self, fg_color="#F4F4F4", corner_radius=15)
        self.card_frame.grid(row=2, column=0, sticky="nsew")
        self.card_frame.grid_columnconfigure(0, weight=1)
        self.card_frame.grid_rowconfigure(2, weight=1)

        self.lbl_subtitulo = ctk.CTkLabel(self.card_frame, text="Registro de Sesiones", font=("Arial", 17, "bold", "italic"), text_color="#006B4D")
        self.lbl_subtitulo.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        self.tabla_header = ctk.CTkFrame(self.card_frame, fg_color="#7A1B6C", corner_radius=8, height=40)
        self.tabla_header.grid(row=1, column=0, padx=(20, 35), pady=(0, 5), sticky="ew")
        self.tabla_header.grid_columnconfigure(list(range(4)), weight=1, uniform="col")
        self.tabla_header.pack_propagate(False)
        
        columnas = ["Nombre", "Telefono", "Estatus", "Editar"]
        for i, col in enumerate(columnas):
            lbl = ctk.CTkLabel(self.tabla_header, text=col, text_color="white", font=("Arial", 14, "bold"), anchor="center")
            lbl.grid(row=0, column=i, pady=10, sticky="ew")

        self.scroll_tabla = ctk.CTkScrollableFrame(self.card_frame, fg_color="transparent")
        self.scroll_tabla.grid(row=2, column=0, padx=15, pady=(0, 20), sticky="nsew")
        self.refrescar_tabla()
                
    
    def fecha_a_texto(self, fecha_str: str) -> str:
        meses = [
            "enero", "febrero", "marzo", "abril",
            "mayo", "junio", "julio", "agosto",
            "septiembre", "octubre", "noviembre", "diciembre"
        ]

        try:
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
            return f"{fecha.day} de {meses[fecha.month - 1]} de {fecha.year}"
        except ValueError:
            raise ValueError("La fecha debe tener el formato AAAA-MM-DD")

    def refrescar_tabla(self):
        for widget in self.scroll_tabla.winfo_children():
            widget.destroy()

        datos_ejemplo = service_obtener_citas_usuarias()
        
        # Diccionario para almacenar la cita más reciente por usuaria
        citas_mas_recientes = {}

        for fila in datos_ejemplo:
            if fila[4] in ("Programada", "Atendida"):
                nombre_usuaria = fila[0]
                fecha_str = fila[1]
                hora_str = fila[3] # Extraemos la hora (basado en tu función crear_tarjeta_sesion)
                
                # Transformamos la fecha Y LA HORA a formato de tiempo para compararla con exactitud
                fecha_hora_str = f"{fecha_str} {hora_str}"
                
                try:
                    # Ajusta "%H:%M" o "%H:%M:%S" dependiendo de cómo guardes la hora en tu base de datos
                    fecha_cita = datetime.strptime(fecha_hora_str, "%Y-%m-%d %H:%M")
                except ValueError:
                    # Fallback por si alguna cita no tiene hora válida
                    fecha_cita = datetime.strptime(fecha_str, "%Y-%m-%d")
                
                # Comparamos
                if nombre_usuaria not in citas_mas_recientes:
                    citas_mas_recientes[nombre_usuaria] = (fila, fecha_cita)
                else:
                    fecha_guardada = citas_mas_recientes[nombre_usuaria][1]
                    # Al incluir la hora, la cita más tarde ese mismo día sí será mayor (>)
                    if fecha_cita > fecha_guardada:
                        citas_mas_recientes[nombre_usuaria] = (fila, fecha_cita)

        lista_ordenada = sorted(
            citas_mas_recientes.values(),
            key=lambda data: 0 if data[0][4] == "Programada" else 1
        )
        # Dibujamos la tabla utilizando únicamente los datos ya filtrados por fecha reciente
        for data in lista_ordenada:
            fila_reciente = data[0]
            
            row_frame = ctk.CTkFrame(self.scroll_tabla, fg_color="white", border_width=1, border_color="#E0E0E0", corner_radius=6, height=40)
            row_frame.pack(fill="x", pady=3, padx=5)
            
            row_frame.grid_columnconfigure(list(range(4)), weight=1, uniform="col")
            row_frame.grid_propagate(False)

            # 0=Nombre, 2=Teléfono, 4=Estatus
            indices_a_mostrar = [0, 2, 4] 

            for col_visual, index_datos in enumerate(indices_a_mostrar):
                color_texto = "#32CD32" if index_datos == 4 and fila_reciente[4] == "Programada" else "black"
                texto_celda = str(fila_reciente[index_datos])
                
                if index_datos == 0 and len(texto_celda) > 18:
                    texto_celda = texto_celda[:15] + "..."
                    
                lbl_dato = ctk.CTkLabel(row_frame, text=texto_celda, text_color=color_texto, font=("Arial", 13), anchor="center")
                lbl_dato.grid(row=0, column=col_visual, pady=8, sticky="ew")
            
            btn_editar = ctk.CTkButton(row_frame, text="Editar Observaciones", width=30, height=24, fg_color="#7A1B6C", hover_color="#E55B2B", text_color="white", corner_radius=5, command=lambda f=fila_reciente: self.abrir_modal(f))
            btn_editar.grid(row=0, column=3, pady=8)
            
    def abrir_modal(self, fila):
        nombre_usuaria = fila[0]
        
        todas_las_citas = service_obtener_citas_usuarias()
        citas_usuaria = [c for c in todas_las_citas if c[0] == nombre_usuaria and c[4] in ("Programada", "Atendida")]
        
        citas_usuaria.sort(key=lambda x: datetime.strptime(x[1], "%Y-%m-%d"), reverse=True)

        modal = ctk.CTkToplevel(self)
        modal.geometry("500x450")
        
        modal.overrideredirect(True) 
        modal.attributes("-topmost", True)
        modal.configure(fg_color="#D3D3D3") 
        
        modal.update_idletasks()
        x = self.winfo_rootx() + (self.winfo_width() // 2) - (600 // 2)
        y = self.winfo_rooty() + (self.winfo_height() // 2) - (550 // 2)
        modal.geometry(f"+{x}+{y}")

        container = ctk.CTkFrame(modal, fg_color="white", corner_radius=10, border_width=1, border_color="#A0A0A0")
        container.pack(fill="both", expand=True)

        header = ctk.CTkFrame(container, fg_color="#FF6B35", corner_radius=8, height=45)
        header.pack(fill="x", padx=1, pady=1)
        header.pack_propagate(False)

        lbl_modal_title = ctk.CTkLabel(header, text="Historial de Sesiones", font=("Arial", 17, "bold", "italic"), text_color="white")
        lbl_modal_title.pack(side="left", padx=15)

        btn_close = ctk.CTkButton(header, text="X", font=("Arial", 19, "bold"), text_color="white", fg_color="transparent", hover_color="#E55A2B", width=30, command=modal.destroy)
        btn_close.pack(side="right", padx=10)

        content = ctk.CTkFrame(container, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=25, pady=15)

        ctk.CTkLabel(content, text=nombre_usuaria, font=("Arial", 19, "bold", "italic"), text_color="#7A1B6C").pack(anchor="w")
        ctk.CTkLabel(content, text="Seleccione una sesión para agregar o visualizar la observación.", font=("Arial", 13, "italic"), text_color="gray").pack(anchor="w", pady=(0, 15))

        self.scroll_sesiones = ctk.CTkScrollableFrame(content, fg_color="transparent")
        self.scroll_sesiones.pack(fill="both", expand=True)

        for cita in citas_usuaria:
            self.crear_tarjeta_sesion(self.scroll_sesiones, cita, modal)

    def crear_tarjeta_sesion(self, parent, cita, modal):
        cita_id = cita[5]
        fecha_cita = cita[1]
        hora = cita[3]

        sesiones_existentes = service_obtener_sesiones_por_cita(cita_id)
        sesion_actual = sesiones_existentes[0] if sesiones_existentes else None
        tiene_observacion = sesion_actual is not None and bool(sesion_actual.observaciones)

        tarjeta = ctk.CTkFrame(parent, fg_color="#F9F9F9", corner_radius=8, border_width=1, border_color="#D3D3D3")
        tarjeta.pack(fill="x", pady=6, padx=5)

        header_tarjeta = ctk.CTkFrame(tarjeta, fg_color="transparent")
        header_tarjeta.pack(fill="x", padx=15, pady=10)

        fecha_texto = self.fecha_a_texto(fecha_cita)
        lbl_info = ctk.CTkLabel(header_tarjeta, text=f"📅 {fecha_texto}   🕒 {hora}", font=("Arial", 14, "bold"), text_color="#333333")
        lbl_info.pack(side="left")

        texto_boton = "Ver observación" if tiene_observacion else "Editar observación"
        color_boton = "#006B4D" if tiene_observacion else "#7A1B6C"
        hover_boton = "#004E38" if tiene_observacion else "#5A134F"

        expand_frame = ctk.CTkFrame(tarjeta, fg_color="transparent")
        is_expanded = {"value": False}

        def toggle_expand():
            if is_expanded["value"]:
                expand_frame.pack_forget()
                is_expanded["value"] = False
            else:
                expand_frame.pack(fill="x", padx=15, pady=(0, 10))
                is_expanded["value"] = True

        btn_accion = ctk.CTkButton(header_tarjeta, text=texto_boton, fg_color=color_boton, hover_color=hover_boton, width=130, height=28, font=("Arial", 12, "bold"), command=toggle_expand)
        btn_accion.pack(side="right")

        txt_obs = ctk.CTkTextbox(expand_frame, height=90, fg_color="white", text_color="black", border_width=1, border_color="#B0B0B0", font=("Arial", 13))
        txt_obs.pack(fill="x", pady=5)

        if tiene_observacion:
            txt_obs.insert("0.0", sesion_actual.observaciones)
            txt_obs.configure(state="disabled", fg_color="#EBEBEB")
        else:
            btn_guardar = ctk.CTkButton(expand_frame, text="Confirmar y Guardar", fg_color="#FF6B35", hover_color="#E55A2B", text_color="white", font=("Arial", 13, "bold"), command=lambda: self.guardar_obs(txt_obs, cita_id, fecha_cita, btn_accion, btn_guardar, sesion_actual, modal))
            btn_guardar.pack(side="right", pady=5)
            
    def guardar_obs(self, textbox, id_c, fecha, btn_acc, btn_g, sesion_actual, modal):
        obs = textbox.get("0.0", "end").strip()
        if not obs:
            messagebox.showwarning("Atención", "La observación no puede estar vacía.", parent=modal) 
            return
            
        confirmacion = messagebox.askyesno(
            "Confirmación", 
            "Una vez guardada la observación, ésta pasará a modo de solo lectura y no podrá ser editada de nuevo.\n\n¿Desea guardar la información permanentemente?",
            parent=modal
        )
        
        if confirmacion:
            if sesion_actual:
                sesion_actual.observaciones = obs
                res = service_actualizar_sesion(sesion_actual)
            else:
                nueva_sesion = Sesion(cita_id=id_c, fecha_sesion=fecha, observaciones=obs)
                res = service_crear_sesion(nueva_sesion)
                
            if res.get("success"):
                messagebox.showinfo("Éxito", "Observación guardada correctamente.", parent=modal)
                textbox.configure(state="disabled", fg_color="#EBEBEB")
                btn_g.pack_forget()  # Oculta el botón de guardar
                btn_acc.configure(text="Ver observación", fg_color="#006B4D", hover_color="#004E38") 
            else:
                messagebox.showerror("Error", f"No se pudo guardar la información: {res.get('error')}", parent=modal)