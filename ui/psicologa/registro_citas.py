import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox
from services.citas_services import service_obtener_citas_usuarias, service_crear_cita, service_actualizar_cita, service_obtener_cita_por_id
from services.usuarias_services import service_obtener_usuarias, service_obtener_usuaria_por_telefono, service_obtener_usuaria_por_id
from services.whatsapp_services import enviar_mensaje_a_usuaria, obtener_estado_servidor
from services.notificaciones_services import service_registrar_envio_whatsapp
from models.cita_model import Cita

class RegistroCitas(ctk.CTkFrame):
    def __init__(self, master, on_actualizar=None):
        super().__init__(master, fg_color="transparent")
        self.on_actualizar = on_actualizar
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
        
        columnas = ["Nombre", "Fecha", "Telefono", "Hora", "Estatus", "Editar"]
        for i, col in enumerate(columnas):
            lbl = ctk.CTkLabel(self.tabla_header, text=col, text_color="white", font=("Arial", 13, "bold"), anchor="center")
            lbl.grid(row=0, column=i, pady=10, sticky="ew")

        self.scroll_tabla = ctk.CTkScrollableFrame(self.card_frame, fg_color="transparent", height=160)
        self.scroll_tabla.grid(row=2, column=0, columnspan=2, padx=15, pady=(0, 10), sticky="ew")

        self.refrescar_tabla()

        self.lbl_subtitulo2 = ctk.CTkLabel(self.card_frame, text="Registrar Nueva Cita", font=("Arial", 16, "bold", "italic"), text_color="#006B4D")
        self.lbl_subtitulo2.grid(row=3, column=0, columnspan=2, padx=20, pady=(20, 10), sticky="w")

        lbl_kwargs = {"font": ("Arial", 12, "bold"), "text_color": "#4A4A4A"}
        opt_kwargs = {"fg_color": "white", "text_color": "black", "button_color": "#E6E6E6", "button_hover_color": "#D3D3D3", 
                      "dropdown_fg_color": "white", "dropdown_text_color": "black", "dropdown_hover_color": "#F0F0F0", 
                      "corner_radius": 6, "height": 38}

        ctk.CTkLabel(self.card_frame, text="Seleccionar Usuaria:", **lbl_kwargs).grid(row=4, column=0, padx=(20, 10), pady=(10, 0), sticky="w")
        
        usuarias = service_obtener_usuarias()
        lista_usuarias = []
        for u in usuarias:
            lista_usuarias.append(u.nombre + " - " + u.telefono)
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

        self.opt_hora = ctk.CTkOptionMenu(self.frame_horario, values=[str(i).zfill(2) for i in range(8, 17)], width=85, **opt_kwargs)
        self.opt_hora.set("Hora")
        self.opt_hora.pack(side="left", padx=(0, 5))

        ctk.CTkLabel(self.frame_horario, text=":", font=("Arial", 16, "bold"), text_color="black").pack(side="left")

        self.opt_minuto = ctk.CTkOptionMenu(self.frame_horario, values=["00", "15", "30", "45"], width=85, **opt_kwargs)
        self.opt_minuto.set("Min.")
        self.opt_minuto.pack(side="left", padx=(5, 0))

        self.btn_registrar = ctk.CTkButton(self.card_frame, text="+ Registrar Cita", fg_color="#FF6B35", text_color="white", font=("Arial", 14, "bold"), corner_radius=8, height=40, command=self.guardar_registro)
        self.btn_registrar.grid(row=7, column=1, padx=20, pady=(10, 30), sticky="e")

    def guardar_registro(self):
        dia = self.opt_dia.get()
        mes = self.opt_mes.get()
        anio = self.opt_ano.get()

        if dia == "Día" or mes == "Mes" or anio == "Año":
            messagebox.showwarning("Faltan datos", "Por favor, seleccione una fecha válida.")
            return
        
        hora = self.opt_hora.get()
        min = self.opt_minuto.get()

        if hora == "Hora" or min == "Min.":
            messagebox.showwarning("Faltan datos", "Por favor, seleccione una hora válida.")
            return
        
        meses_dict = {"Enero": "01", "Febrero": "02", "Marzo": "03", "Abril": "04", "Mayo": "05", "Junio": "06", "Julio": "07", "Agosto": "08", "Septiembre": "09", "Octubre": "10", "Noviembre": "11", "Diciembre": "12"}
        fecha_cita = f"{anio}-{meses_dict[mes]}-{dia}"
        hora_cita = f"{hora}:{min}"

        usuaria_telefono = self.opt_usuaria.get()
        datos_usuaria = usuaria_telefono.split(" - ")
        usuaria_info = service_obtener_usuaria_por_telefono(datos_usuaria[1])

        nueva_cita = Cita(
            fecha=fecha_cita,
            hora=hora_cita,
            estado_id=1,    #Activa
            usuaria_id=usuaria_info.id_usuaria,
            psicologa_id=1, #Se toma del usuario_sistema
        )

        confirmacion = messagebox.askyesno("Confirmar Cita", f"¿Está segura de que desea agendar una cita para {datos_usuaria[0]}?")
        
        if not confirmacion:
            return

        res_cita = service_crear_cita(nueva_cita)
        if res_cita["success"]:
            self.refrescar_tabla()
            if self.on_actualizar:
                self.on_actualizar()
            estado_servidor_whatsapp = obtener_estado_servidor()
            if estado_servidor_whatsapp["status"] == "connected":
                cita_info = service_obtener_cita_por_id(res_cita["id_cita"])
                usuaria_info = service_obtener_usuaria_por_id(cita_info.usuaria_id)
                envio_mensaje = enviar_mensaje_a_usuaria(usuaria_info, cita_info, "nueva_cita")
                if envio_mensaje["success"]:
                    service_registrar_envio_whatsapp(cita_id=cita_info.id_cita, mensaje=envio_mensaje["mensaje"])
                    messagebox.showinfo("Éxito", "¡Cita agendada correctamente!")
                else:
                    messagebox.showwarning("Aviso", f"Cita agendada, pero falló el envío de confirmación por Whatsapp: {envio_mensaje.get('error')}")
            else:
                messagebox.showwarning("Aviso", f"Cita agendada, pero falló el envío de confirmación por Whatsapp: No se pudo conectar con el servidor de Whatsapp.")
            self.limpiar_formulario()
            return
        else:
            messagebox.showerror("Error al agendar la cita.", res_cita.get("error"))
            self.limpiar_formulario()
            return

    def limpiar_formulario(self):
        self.opt_dia.set("Día")
        self.opt_mes.set("Mes")
        self.opt_ano.set("Año")
        self.opt_hora.set("Hora")
        self.opt_minuto.set("Min.")

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

    def abrir_modal_editar(self, datos_fila):
        nombre, fecha, telefono, hora, estatus, id_cita = datos_fila

        modal = ctk.CTkToplevel(self)
        modal.title("Editar Cita")
        modal.geometry("400x520")
        modal.resizable(False, False)
        
        modal.transient(self.winfo_toplevel())
        modal.grab_set()

        ctk.CTkLabel(modal, text="Editar Cita", font=("Arial", 24, "bold"), text_color="#7A1B6C").pack(pady=(20, 15))

        entry_style = {"fg_color": "white", "text_color": "black", "border_width": 1, "border_color": "#D3D3D3", "corner_radius": 6, "height": 35}

        def crear_input_modal(texto, valor_inicial, editable=True):
            ctk.CTkLabel(modal, text=texto, font=("Arial", 12, "bold"), text_color="#555555").pack(anchor="w", padx=40)
            ent = ctk.CTkEntry(modal, **entry_style)
            ent.insert(0, valor_inicial) 
            
            if not editable:
                ent.configure(state="disabled", fg_color="#EBEBEB", text_color="#7A7A7A")
                
            ent.pack(fill="x", padx=40, pady=(0, 10))
            return ent

        ent_nombre = crear_input_modal("Nombre:", nombre, editable=False)
        ent_telefono = crear_input_modal("Teléfono:", telefono, editable=False)
        ent_fecha = crear_input_modal("Fecha:", fecha, editable=True)
        ent_hora = crear_input_modal("Hora (HH:MM):", hora, editable=True)
        
        ctk.CTkLabel(modal, text="Estatus:", font=("Arial", 12, "bold"), text_color="#555555").pack(anchor="w", padx=40)
        opt_estatus = ctk.CTkOptionMenu(modal, values=["Activa", "Completada", "Cancelada"], fg_color="white", text_color="black", button_color="#E6E6E6", button_hover_color="#D3D3D3", dropdown_fg_color="white", dropdown_text_color="black", corner_radius=6, height=35)
        opt_estatus.set(estatus) 
        opt_estatus.pack(fill="x", padx=40, pady=(0, 10))

        lbl_mensaje = ctk.CTkLabel(modal, text="", font=("Arial", 12, "bold"))
        lbl_mensaje.pack(pady=(5, 0))

        def guardar_modificacion():
            cita_actual = service_obtener_cita_por_id(id_cita=id_cita)
            if ent_fecha.get() != cita_actual.fecha or ent_hora.get() != cita_actual.hora:
                cita_modificada = Cita(
                    ent_fecha.get(),
                    cita_actual.usuaria_id,
                    cita_actual.psicologa_id,
                    ent_hora.get(),
                    cita_actual.estado_id,
                    cita_actual.id_cita
                )
                res_actualizar_cita = service_actualizar_cita(cita_modificada)
                if res_actualizar_cita["success"]:
                    self.refrescar_tabla()
                    if self.on_actualizar:
                        self.on_actualizar()
                    estado_servidor_whatsapp = obtener_estado_servidor()
                    if estado_servidor_whatsapp["status"] == "connected":
                        usuaria_info =  service_obtener_usuaria_por_id(cita_actual.usuaria_id)
                        envio_mensaje = enviar_mensaje_a_usuaria(usuaria_info, cita_modificada, "reagendar_cita")
                        if envio_mensaje["success"]:
                            service_registrar_envio_whatsapp(cita_id=cita_modificada.id_cita, mensaje=envio_mensaje["mensaje"])
                            lbl_mensaje.configure(text="✅ Cita actualizada correctamente", text_color="#32CD32")
                        else:
                            lbl_mensaje.configure(text="Cita actualizada, pero error al enviar notificación: " + envio_mensaje["error"], text_color="#B65F18")
                    else:
                        lbl_mensaje.configure(text="Cita actualizada, pero error al enviar notificación: No se pudo conectar con el servidor de Whatsapp", text_color="#B65F18")
                    self.after(1500, modal.destroy)
                else:
                    lbl_mensaje.configure(text="Ha ocurrido un error: " + res_actualizar_cita["error"], text_color="#A80A0A")
                    self.after(1500, modal.destroy)
            else:
                # No hubo cambios
                self.after(500, modal.destroy)

        btn_guardar = ctk.CTkButton(modal, text="Aceptar modificación", command=guardar_modificacion, fg_color="#FF6B35", hover_color="#E55B2B", text_color="white", font=("Arial", 14, "bold"), corner_radius=8, height=40)
        btn_guardar.pack(pady=(10, 20))
        
    def refrescar_tabla(self):
        for widget in self.scroll_tabla.winfo_children():
            widget.destroy()

        datos_ejemplo = service_obtener_citas_usuarias()

        for fila in datos_ejemplo:
            if fila[4] == "Activa":
                row_frame = ctk.CTkFrame(self.scroll_tabla, fg_color="white", border_width=1, border_color="#E0E0E0", corner_radius=6, height=40)
                row_frame.pack(fill="x", pady=3, padx=5)
                row_frame.grid_columnconfigure(list(range(6)), weight=1, uniform="col")
                row_frame.grid_propagate(False)

                for i in range(5):
                    color_texto = "#32CD32" if fila[4] == "Activa" and i == 4 else "black"
                    lbl_dato = ctk.CTkLabel(row_frame, text=fila[i], text_color=color_texto, font=("Arial", 12), anchor="center")
                    lbl_dato.grid(row=0, column=i, pady=8, sticky="ew")
                
                btn_editar = ctk.CTkButton(row_frame, text="Editar ✏️", width=30, height=24, fg_color="#7A1B6C", hover_color="#E55B2B", text_color="white", corner_radius=5, 
                                        command=lambda f=fila: self.abrir_modal_editar(f))
                btn_editar.grid(row=0, column=5, pady=8)