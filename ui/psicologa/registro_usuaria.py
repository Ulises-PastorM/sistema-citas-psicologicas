import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from models.usuaria_model import Usuaria
from models.direccion_model import Direccion
from models.agresor_model import Agresor
from services.usuarias_services import (
    service_crear_usuaria,
    service_crear_usuaria_direccion,
    service_obtener_usuarias,
    service_obtener_usuaria_por_telefono,
    service_obtener_usuaria_direccion,
    service_obtener_usuaria_agresor,
    service_actualizar_usuaria)
from services.direcciones_services import (
    service_crear_direccion,
    service_obtener_direccion_por_id,
    service_actualizar_direccion)
from repositories.catalogos_repository import (
    obtener_domicilio_estatus,
    obtener_escolaridades,
    obtener_estados_civiles,
    obtener_lenguas_indigenas,
    obtener_roles,
    obtener_servicios_immujer,
    obtener_sexos,
    obtener_estatus
)
from services.agresores_services import (
    service_actualizar_agresor,
    service_crear_y_vincular_agresor,
    service_obtener_agresor_por_id
)

class RegistroUsuariaView(ctk.CTkFrame):
    def __init__(self, master, on_actualizar=None):
        super().__init__(master, fg_color="transparent")
        
        self.on_actualizar = on_actualizar
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.datos_domicilio = None
        self.datos_agresor = None
        self.padecimientos_seleccionados = [] 
        self.editando_usuaria = False
        self.id_usuaria_editada = 0
        self.id_direccion_editada = 0
        self.id_agresor_editado = 0
        self.btn_submit = None
        self.domicilio_estatus_list = None
        self.escolaridades_list = None
        self.estados_civiles_list = None
        self.lenguas_indigenas_list = None
        self.roles_list = None
        self.servicios_immujer_list = None
        self.sexos_list = None
        self.estatus_list = None
        
        self.lista_padecimientos = [
            "Diabetes", "Hipertensión", "Obesidad", "Enfermedades cardiovasculares", "Asma",
            "Enfermedad renal crónica", "Enfermedades de la tiroides", "Artritis", "Gastritis", "Otro"
        ]

        self.lbl_titulo = ctk.CTkLabel(self, text="Registro de Usuaria para Atención Psicológica", font=("Arial", 21, "bold", "italic"), text_color="#006B4D")
        self.lbl_titulo.grid(row=0, column=0, pady=(0, 10), sticky="w")
        
        self.btn_volver_inicio = ctk.CTkButton(self, text=" 🡨 Volver a opciones", command=self.volver_al_inicio, fg_color="#FF6B35", font=("Arial", 15, "bold"), text_color="white")
        self.btn_volver_inicio.grid(row=0, column=0, pady=(0, 10), sticky="e")
        self.btn_volver_inicio.grid_remove() # Lo ocultamos inicialmente

        self.card_frame = ctk.CTkFrame(self, fg_color="#F4F4F4", corner_radius=15)
        self.card_frame.grid(row=1, column=0, sticky="nsew")
        self.card_frame.grid_rowconfigure(0, weight=1)
        self.card_frame.grid_columnconfigure(0, weight=1)
        

        self.entry_style = {
            "fg_color": "white", 
            "text_color": "black", 
            "border_width": 1, 
            "border_color": "#D3D3D3", 
            "corner_radius": 8, 
            "height": 35
        }
        
        self.option_style = {
            "fg_color": "white", 
            "text_color": "black", 
            "button_color": "#E0E0E0", 
            "button_hover_color": "#D3D3D3", 
            "dropdown_fg_color": "white", 
            "dropdown_text_color": "black", 
            "corner_radius": 8, 
            "height": 35
        }
        
        self.btn_nav_style = {
            "fg_color": "#FF6B35", 
            "text_color": "white", 
            "font": ("Arial", 19, "bold"), 
            "width": 40, 
            "height": 35, 
            "corner_radius": 8
        }

        self.vcmd_numeros = (self.register(self.solo_numeros), '%P')

        self.cargar_catalogos()
        self.crear_pagina_inicio()
        self.crear_pagina_1()
        self.crear_pagina_2()
        self.crear_pagina_3()

        self.mostrar_pagina(self.page_inicio)

    def solo_numeros(self, texto_propuesto):
        return texto_propuesto.isdigit() or texto_propuesto == ""

    def mostrar_pagina(self, pagina):
        # Ocultamos todas las páginas de la cuadrícula
        if hasattr(self, 'page_inicio'): self.page_inicio.grid_forget()
        if hasattr(self, 'page1'): self.page1.grid_forget()
        if hasattr(self, 'page2'): self.page2.grid_forget()
        if hasattr(self, 'page3'): self.page3.grid_forget()
        
        # Solo volvemos a dibujar la que queremos ver
        pagina.grid(row=0, column=0, sticky="nsew", padx=30, pady=15)
    
    def crear_pagina_inicio(self):
        self.page_inicio = ctk.CTkFrame(self.card_frame, fg_color="transparent")
        self.page_inicio.grid_columnconfigure((0, 1), weight=1)
        self.page_inicio.grid_rowconfigure(0, weight=1)

        contenedor_botones = ctk.CTkFrame(self.page_inicio, fg_color="transparent")
        contenedor_botones.grid(row=0, column=0, columnspan=2, pady=180)
        contenedor_botones.grid_columnconfigure((0, 1), weight=1)
        from PIL import Image
        icono_registro = ctk.CTkImage(light_image=Image.open("assets/add.png"), size=(60, 60))
        icono_actualizar = ctk.CTkImage(light_image=Image.open("assets/edit.png"), size=(60, 60))

        btn_registrar = ctk.CTkButton(
            contenedor_botones,
            text="Registrar Nueva Usuaria", 
            font=("Arial", 19, "bold"),
            fg_color="#006B4D",
            hover_color="#004E38", 
            text_color="white",
            height=120,
            width=360,
            corner_radius=15,
            image=icono_registro, 
            command=self.iniciar_registro_nuevo
        )
        btn_registrar.grid(row=0, column=0, padx=(0, 20), sticky="e")

        btn_actualizar = ctk.CTkButton(
            contenedor_botones,
            text="Actualizar Datos de Usuaria", 
            font=("Arial", 19, "bold"),
            fg_color="#FF6B35",
            hover_color="#CC552A", 
            text_color="white",
            height=120,
            width=360,
            corner_radius=15,
            image=icono_actualizar, 
            command=self.abrir_modal_busqueda
        )
        btn_actualizar.grid(row=0, column=1, padx=(20, 0), sticky="w")

    def iniciar_registro_nuevo(self):
        self.editando_usuaria = False
        self.limpiar_formulario()
        self.refrescar_boton_registrar_editar()
        self.btn_volver_inicio.grid()
        self.mostrar_pagina(self.page1) 

    def volver_al_inicio(self):
        self.btn_volver_inicio.grid_remove()
        self.mostrar_pagina(self.page_inicio)

    def crear_campo_entrada(self, parent, texto_label, ancho=None, validacion=None, color="#555555"):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        ctk.CTkLabel(frame, text=texto_label, text_color=color, font=("Arial", 13, "bold")).pack(anchor="w", pady=(0, 2))
        
        estilo = self.entry_style.copy()
        if ancho:
            estilo["width"] = ancho
            
        entry = ctk.CTkEntry(frame, **estilo)
        
        if validacion:
            entry.configure(validate="key", validatecommand=validacion)

        if ancho:
            entry.pack(anchor="w")
        else:
            entry.pack(fill="x", expand=True)

        return frame, entry

    def crear_campo_opciones(self, parent, texto_label, opciones):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        ctk.CTkLabel(frame, text=texto_label, text_color="#555555", font=("Arial", 13, "bold")).pack(anchor="w", pady=(0, 2))
        
        menu = ctk.CTkOptionMenu(frame, values=opciones, **self.option_style)
        menu.pack(fill="x", expand=True)
        return frame, menu

    def crear_campo_boton(self, parent, texto_label, texto_boton, comando):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        ctk.CTkLabel(frame, text=texto_label, text_color="#555555", font=("Arial", 13, "bold")).pack(anchor="w", pady=(0, 2))
        
        btn = ctk.CTkButton(frame, text=texto_boton, command=comando,
                            fg_color="white", text_color="gray", hover_color="#F0F0F0",
                            border_width=1, border_color="#D3D3D3",
                            corner_radius=8, height=35, anchor="w")
        btn.pack(fill="x", expand=True)
        return frame, btn
    
    def cargar_catalogos(self):
        try:
            self.domicilio_estatus_list = obtener_domicilio_estatus()
            self.escolaridades_list = obtener_escolaridades()
            self.estados_civiles_list = obtener_estados_civiles()
            self.lenguas_indigenas_list = obtener_lenguas_indigenas()
            self.roles_list = obtener_roles()
            self.servicios_immujer_list = obtener_servicios_immujer()
            self.sexos_list = obtener_sexos()
            self.estatus_list = obtener_estatus()
        except Exception as e:
            print(f"[cargar_catalogos] Error al cargar catálogos: {e}")
            return

    def crear_pagina_1(self):
        self.page1 = ctk.CTkFrame(self.card_frame, fg_color="transparent")
        self.page1.grid(row=0, column=0, sticky="nsew", padx=30, pady=15)
        self.page1.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(self.page1, text="Registrar Usuaria", font=("Arial", 15, "bold", "italic"), text_color="#006B4D").grid(row=0, column=0, sticky="w", pady=(0, 10))

        f_nom, self.ent_nombre = self.crear_campo_entrada(self.page1, "Nombre completo (*):", color="#D60D0D")
        f_nom.grid(row=1, column=0, sticky="ew", padx=(0, 10), pady=(0, 12))
        
        escolaridades = [e.escolaridad for e in self.escolaridades_list]
        f_esc, self.opt_escolaridad = self.crear_campo_opciones(self.page1, "Escolaridad:", escolaridades)
        f_esc.grid(row=1, column=1, sticky="ew", padx=(10, 0), pady=(0, 12))
        
        f_fec = ctk.CTkFrame(self.page1, fg_color="transparent")
        f_fec.grid(row=2, column=0, sticky="ew", padx=(0, 10), pady=(0, 12))
        ctk.CTkLabel(f_fec, text="Fecha de nacimiento (*):", text_color="#D60D0D", font=("Arial", 13, "bold")).pack(anchor="w", pady=(0, 2))
        
        f_fec_inputs = ctk.CTkFrame(f_fec, fg_color="transparent")
        f_fec_inputs.pack(fill="x", expand=True)
        
        dias = [str(i).zfill(2) for i in range(1, 32)] 
        meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
        anos = [str(i) for i in range(2026, 1920, -1)] 
        
        dias.insert(0, "Día")
        meses.insert(0, "Mes")
        anos.insert(0, "Año")

        self.opt_dia = ctk.CTkOptionMenu(f_fec_inputs, values=dias, width=70, **self.option_style)
        self.opt_dia.pack(side="left", padx=(0, 5))
        
        self.opt_mes = ctk.CTkOptionMenu(f_fec_inputs, values=meses, width=80, **self.option_style)
        self.opt_mes.pack(side="left", padx=(0, 5))
        
        self.opt_ano = ctk.CTkOptionMenu(f_fec_inputs, values=anos, width=80, **self.option_style)
        self.opt_ano.pack(side="left")
        
        sexos = [s.sexo for s in self.sexos_list]
        f_sex, self.opt_sexo = self.crear_campo_opciones(self.page1, "Sexo:", sexos)
        f_sex.grid(row=2, column=1, sticky="ew", padx=(10, 0), pady=(0, 12))
        
        f_lug, self.ent_lugar = self.crear_campo_entrada(self.page1, "Lugar de nacimiento:")
        f_lug.grid(row=3, column=0, sticky="ew", padx=(0, 10), pady=(0, 12))
        
        lenguas_indigenas = [l.lengua_indigena for l in self.lenguas_indigenas_list]
        f_len, self.opt_lengua = self.crear_campo_opciones(self.page1, "Lengua indígena:", lenguas_indigenas)
        f_len.grid(row=3, column=1, sticky="ew", padx=(10, 0), pady=(0, 12))

        f_ocu, self.ent_ocupacion = self.crear_campo_entrada(self.page1, "Ocupación:")
        f_ocu.grid(row=4, column=0, sticky="ew", padx=(0, 10), pady=(0, 12))
        
        f_pad, self.btn_padecimiento = self.crear_campo_boton(self.page1, "Padecimiento(s):", "📍 Seleccionar padecimientos...", self.abrir_modal_padecimientos)
        f_pad.grid(row=4, column=1, sticky="ew", padx=(10, 0), pady=(0, 12))
        
        f_tel, self.ent_telefono = self.crear_campo_entrada(self.page1, "Número de teléfono (*):", validacion=self.vcmd_numeros, color="#D60D0D")
        f_tel.grid(row=5, column=0, sticky="ew", padx=(0, 10), pady=(0, 12))
        
        f_dom, self.btn_domicilio = self.crear_campo_boton(self.page1, "Domicilio:", "📍 Ingresar Domicilio...", self.abrir_modal_domicilio)
        f_dom.grid(row=5, column=1, sticky="ew", padx=(10, 0), pady=(0, 12))
        
        estados_civiles = [ec.estado_civil for ec in self.estados_civiles_list]
        f_civ, self.opt_civil = self.crear_campo_opciones(self.page1, "Estado civil:", estados_civiles)
        f_civ.grid(row=6, column=0, sticky="ew", padx=(0, 10), pady=(0, 12))
        
        btn_next = ctk.CTkButton(self.page1, text="➔", command=lambda: self.mostrar_pagina(self.page2), **self.btn_nav_style)
        btn_next.grid(row=6, column=1, sticky="e", pady=(5, 10))
        
    def abrir_modal_padecimientos(self):
        modal = ctk.CTkToplevel(self)
        modal.title("Seleccionar Padecimientos")
        modal.geometry("400x500") 
        modal.resizable(False, False)
        modal.transient(self.winfo_toplevel())
        modal.grab_set()

        ctk.CTkLabel(modal, text="⚕️ Seleccione los padecimientos", font=("Arial", 17, "bold"), text_color="#006B4D").pack(pady=(20, 10))

        scroll_pad = ctk.CTkFrame(modal, fg_color="transparent")
        scroll_pad.pack(fill="both", expand=True, padx=30, pady=(0, 10))

        checkbox_vars = {}

        for pad in self.lista_padecimientos:
            valor_inicial = pad if pad in self.padecimientos_seleccionados else ""
            var = ctk.StringVar(value=valor_inicial)
            checkbox_vars[pad] = var
            
            cb = ctk.CTkCheckBox(scroll_pad, text=pad, variable=var, onvalue=pad, offvalue="", fg_color="#FF6B35", hover_color="#E55A2B", text_color="black")
            cb.pack(anchor="w", pady=5)


        def guardar_padecimientos():
            self.padecimientos_seleccionados = [var.get() for var in checkbox_vars.values() if var.get() != ""]
                
            num_seleccionados = len(self.padecimientos_seleccionados)
            if num_seleccionados > 0:
                self.btn_padecimiento.configure(text=f" ✅ {num_seleccionados} seleccionados", text_color="black", border_color="#32CD32", border_width=2)
            else:
                self.btn_padecimiento.configure(text="📍 Seleccionar padecimientos...", text_color="gray", border_color="#D3D3D3", border_width=1)
                
            modal.destroy()

        ctk.CTkButton(modal, text="Guardar Selección", command=guardar_padecimientos, fg_color="#FF6B35", text_color="white", font=("Arial", 15, "bold"), corner_radius=8, height=35).pack(pady=(0, 20))
        
    def abrir_modal_domicilio(self):
        modal = ctk.CTkToplevel(self)
        modal.title("Detalles del Domicilio")
        modal.geometry("400x450")
        modal.resizable(False, False)
        
        modal.transient(self.winfo_toplevel())
        modal.grab_set()

        ctk.CTkLabel(modal, text="🏠 Dirección y Estatus", font=("Arial", 17, "bold"), text_color="#006B4D").pack(pady=(20, 15))

        ctk.CTkLabel(modal, text="Calle y Número:", text_color="#555555", font=("Arial", 13, "bold")).pack(anchor="w", padx=30)
        ent_calle = ctk.CTkEntry(modal, **self.entry_style)
        ent_calle.pack(fill="x", padx=30, pady=(0, 15))

        ctk.CTkLabel(modal, text="Colonia ó Agencia:", text_color="#555555", font=("Arial", 13, "bold")).pack(anchor="w", padx=30)
        ent_colonia = ctk.CTkEntry(modal, **self.entry_style)
        ent_colonia.pack(fill="x", padx=30, pady=(0, 15))

        ctk.CTkLabel(modal, text="Municipio:", text_color="#555555", font=("Arial", 13, "bold")).pack(anchor="w", padx=30)
        ent_municipio = ctk.CTkEntry(modal, **self.entry_style)
        ent_municipio.pack(fill="x", padx=30, pady=(0, 15))

        domicilio_estatus = [d.domicilio_estatus for d in self.domicilio_estatus_list]
        ctk.CTkLabel(modal, text="Estatus de su domicilio:", text_color="#555555", font=("Arial", 13, "bold")).pack(anchor="w", padx=30)
        opt_estatus = ctk.CTkOptionMenu(modal, values=domicilio_estatus, **self.option_style)
        opt_estatus.pack(fill="x", padx=30, pady=(0, 25))

        if self.datos_domicilio:
            ent_calle.insert(0, self.datos_domicilio.calle_numero)
            ent_colonia.insert(0, self.datos_domicilio.colonia)
            ent_municipio.insert(0, self.datos_domicilio.municipio)
            opt_estatus.set(self._id_a_texto(self.domicilio_estatus_list, "id_domicilio_estatus", self.datos_domicilio.domicilio_estatus_id, "domicilio_estatus"))

        def guardar_datos():
            if ent_calle.get() == "":
                messagebox.showwarning("Faltan datos", "Por favor, ingrese una calle y numero")
                return
            
            if ent_colonia.get() == "":
                messagebox.showwarning("Faltan datos", "Por favor, ingrese una colonia o agencia")
                return
            
            if ent_municipio.get() == "":
                messagebox.showwarning("Faltan datos", "Por favor, ingrese un municipio")
                return

            self.datos_domicilio = Direccion(
                calle_numero = ent_calle.get(),
                colonia = ent_colonia.get(),
                municipio = ent_municipio.get(),
                domicilio_estatus_id = self._texto_a_id(self.domicilio_estatus_list, "domicilio_estatus", opt_estatus.get(), "id_domicilio_estatus"),
                id_direccion = self.id_direccion_editada if self.editando_usuaria else None
            )

            self.btn_domicilio.configure(text=" ✅ Domicilio guardado", text_color="black", border_color="#32CD32", border_width=2)
            modal.destroy()

        btn_guardar = ctk.CTkButton(modal, text="Guardar Datos", command=guardar_datos, fg_color="#FF6B35", text_color="white", font=("Arial", 15, "bold"), corner_radius=8, height=35)
        btn_guardar.pack(pady=(0, 20))

    def crear_pagina_2(self):
        self.page2 = ctk.CTkFrame(self.card_frame, fg_color="transparent")
        self.page2.grid(row=0, column=0, sticky="nsew", padx=30, pady=15)
        self.page2.grid_columnconfigure((0, 1, 2, 3), weight=1)

        ctk.CTkLabel(self.page2, text="Integrantes de la familia", font=("Arial", 15, "bold", "italic"), text_color="#006B4D").grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 10))

        tabla_frame = ctk.CTkFrame(self.page2, fg_color="transparent")
        tabla_frame.grid(row=1, column=0, columnspan=4, sticky="ew", pady=(0, 10))

        tabla_frame.grid_columnconfigure(0, weight=0)
        tabla_frame.grid_columnconfigure(1, weight=1)
        tabla_frame.grid_columnconfigure(2, weight=1)
        tabla_frame.grid_columnconfigure(3, weight=1)

        # Mujeres
        ctk.CTkLabel(tabla_frame, text="Mujeres:", text_color="gray").grid(row=1, column=0, sticky="w", padx=0, pady=2)

        self.ent_mujeres = ctk.CTkEntry(tabla_frame, **self.entry_style)
        self.ent_mujeres.insert(0, "0")
        self.ent_mujeres.grid(row=1, column=1, columnspan=3, padx=(10, 0), pady=2, sticky="ew")

        # Hombres
        ctk.CTkLabel(tabla_frame, text="Hombres:", text_color="gray").grid(row=2, column=0, sticky="w", padx=0, pady=2)

        self.ent_hombres = ctk.CTkEntry(tabla_frame, **self.entry_style)
        self.ent_hombres.insert(0, "0")
        self.ent_hombres.grid(row=2, column=1, columnspan=3, padx=(10, 0), pady=2, sticky="ew")
        
        ctk.CTkFrame(self.page2, height=2, fg_color="#D3D3D3").grid(row=2, column=0, columnspan=4, sticky="ew", pady=10)

        ctk.CTkLabel(self.page2, text="Anteriormente\n¿Acudió a INMUJER?", text_color="gray").grid(row=3, column=0, sticky="e", padx=5)
        self.var_immujer = ctk.StringVar(value="No")
        ctk.CTkRadioButton(self.page2, text="Sí", variable=self.var_immujer, value="Sí", radiobutton_width=15, radiobutton_height=15, command=self.actualizar_campos_immujer).grid(row=3, column=1, sticky="w")
        ctk.CTkRadioButton(self.page2, text="No", variable=self.var_immujer, value="No", radiobutton_width=15, radiobutton_height=15, command=self.actualizar_campos_immujer).grid(row=3, column=1, sticky="e")
        
        f_cua, self.ent_cuando = self.crear_campo_entrada(self.page2, "¿Cuándo?")
        f_cua.grid(row=3, column=2, padx=5, sticky="ew", pady=(0, 10))
        
        f_tip, self.ent_tipo_apoyo = self.crear_campo_entrada(self.page2, "Tipo de apoyo/Asesoría:")
        f_tip.grid(row=3, column=3, padx=5, sticky="ew", pady=(0, 10))

        ctk.CTkLabel(self.page2, text="Anteriormente\n¿Ha recibido terapia?", text_color="gray").grid(row=4, column=0, sticky="e", padx=5, pady=10)
        self.var_terapia = ctk.StringVar(value="No")
        ctk.CTkRadioButton(self.page2, text="Sí", variable=self.var_terapia, value="Sí", radiobutton_width=15, radiobutton_height=15, command=self.actualizar_campos_immujer).grid(row=4, column=1, sticky="w")
        ctk.CTkRadioButton(self.page2, text="No", variable=self.var_terapia, value="No", radiobutton_width=15, radiobutton_height=15, command=self.actualizar_campos_immujer).grid(row=4, column=1, sticky="e")
        
        f_tie, self.ent_tiempo = self.crear_campo_entrada(self.page2, "Tiempo desde última consulta:")
        f_tie.grid(row=4, column=2, padx=5, sticky="ew", pady=(0, 10))

        opciones_lugar = ["Público", "Privado"]

        f_lug_terapia, self.ent_lugar_terapia = self.crear_campo_opciones(self.page2, "Lugar:", opciones_lugar)
        f_lug_terapia.grid(row=4, column=3, padx=5, sticky="ew", pady=(0, 10))

        self.actualizar_campos_immujer()

        dependencias = ["Vicefiscalía", "Procuraduría", "Juzgado familiar", "Hospital", "Otra"]
        f_can, self.opt_canalizada = self.crear_campo_opciones(self.page2, "Canalizada por:", dependencias)
        f_can.grid(row=5, column=0, columnspan=2, padx=5, pady=(0, 10), sticky="ew")
        
        f_red, self.ent_red_apoyo = self.crear_campo_entrada(self.page2, "Red de apoyo (Nombre y Parentesco):")
        f_red.grid(row=5, column=2, columnspan=2, padx=5, pady=(0, 10), sticky="ew")

        btn_prev = ctk.CTkButton(self.page2, text="🡨", command=lambda: self.mostrar_pagina(self.page1), **self.btn_nav_style)
        btn_prev.grid(row=6, column=0, sticky="w", pady=(10, 0))
        
        btn_next = ctk.CTkButton(self.page2, text="➔", command=lambda: self.mostrar_pagina(self.page3), **self.btn_nav_style)
        btn_next.grid(row=6, column=3, sticky="e", pady=(10, 0))

    def crear_pagina_3(self):
        self.page3 = ctk.CTkFrame(self.card_frame, fg_color="transparent")
        self.page3.grid(row=0, column=0, sticky="nsew", padx=30, pady=20)
        self.page3.grid_columnconfigure((0, 1), weight=1)

        f_motivo = ctk.CTkFrame(self.page3, fg_color="transparent")
        f_motivo.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        ctk.CTkLabel(f_motivo, text="Motivo de la consulta (*):", text_color="#D60D0D", font=("Arial", 13, "bold")).pack(anchor="w", pady=(0, 2))
        
        self.txt_motivo = ctk.CTkTextbox(f_motivo, height=100, fg_color="white", text_color="black", border_width=1, border_color="#D3D3D3", corner_radius=8)
        self.txt_motivo.pack(fill="x")

        f_agr, self.ent_agresor = self.crear_campo_entrada(self.page3, "Nombre del agresor:")
        f_agr.grid(row=1, column=0, sticky="ew", padx=(0, 10), pady=(0, 12))
        
        f_par, self.ent_parentesco = self.crear_campo_entrada(self.page3, "Parentesco:")
        f_par.grid(row=1, column=1, sticky="ew", padx=(10, 0), pady=(0, 12))
        
        f_ocua, self.ent_ocupacion_agresor = self.crear_campo_entrada(self.page3, "Ocupación:")
        f_ocua.grid(row=2, column=0, sticky="ew", padx=(0, 10), pady=(0, 12))
        
        f_eda, self.ent_edad_agresor = self.crear_campo_entrada(self.page3, "Edad:", ancho=100, validacion=self.vcmd_numeros)
        f_eda.grid(row=3, column=0, sticky="w", pady=(0, 12))

        if self.datos_agresor:
            self.ent_agresor.insert(0, self.datos_agresor.nombre_agresor)
            self.ent_parentesco.insert(0, self.datos_agresor.parentesco_agresor)
            self.ent_ocupacion_agresor.insert(0, self.datos_agresor.ocupacion_agresor)
            self.ent_edad_agresor.insert(0, self.datos_agresor.edad_agresor)
        
        btn_prev = ctk.CTkButton(self.page3, text="🡨", command=lambda: self.mostrar_pagina(self.page2), **self.btn_nav_style)
        btn_prev.grid(row=4, column=0, sticky="w", pady=(20, 0))

        self.btn_submit = ctk.CTkButton(
            self.page3,
            text="+ Registrar Usuaria",
            fg_color="#FF6B35",
            text_color="white",
            font=("Arial", 16, "bold"),
            height=35,
            corner_radius=8,
            command=self.guardar_registro
        )
        self.btn_submit.grid(row=4, column=1, sticky="e", pady=(20, 0))
        
    
    def actualizar_campos_immujer(self):
        if self.var_immujer.get() == "Sí":
            self.ent_cuando.configure(state="normal", fg_color="white", text_color="black")
            self.ent_tipo_apoyo.configure(state="normal", fg_color="white", text_color="black")
        else:
            self.ent_cuando.configure(state="disabled", fg_color="#EBEBEB", text_color="#7A7A7A")
            self.ent_tipo_apoyo.configure(state="disabled", fg_color="#EBEBEB", text_color="#7A7A7A")
        
        if self.var_terapia.get() == "Sí":
            self.ent_tiempo.configure(state="normal", fg_color="white", text_color="black")
            self.ent_lugar_terapia.configure(state="normal", fg_color="white", text_color="black")
        else:
            self.ent_tiempo.configure(state="disabled", fg_color="#EBEBEB", text_color="#7A7A7A")
            self.ent_lugar_terapia.configure(state="disabled", fg_color="#EBEBEB", text_color="#7A7A7A")

    def refrescar_boton_registrar_editar(self):
        self.btn_submit.configure(
            text="+ Guardar cambios" if self.editando_usuaria else "+ Registrar Usuaria"
        )
    
    def _id_a_texto(self, lista, attr_id, valor_id, attr_texto) -> str:
        item = next((x for x in lista if getattr(x, attr_id) == valor_id), None)
        return getattr(item, attr_texto) if item else "Sin especificar"
    
    def _texto_a_id(self, lista, attr_texto, valor_texto, attr_id) -> int | None:
        item = next((x for x in lista if getattr(x, attr_texto) == valor_texto), None)
        return getattr(item, attr_id) if item else 1

    def guardar_registro(self):
            if self.ent_nombre.get() == "":
                messagebox.showwarning("Faltan datos", "Por favor, ingrese un nombre válido")
                return
            
            if self.ent_telefono.get() == "":
                messagebox.showwarning("Faltan datos", "Por favor, ingrese un telefono válido")
                return
            
            dia = self.opt_dia.get()
            mes = self.opt_mes.get()
            anio = self.opt_ano.get()
            
            if dia == "Día" or mes == "Mes" or anio == "Año":
                messagebox.showwarning("Faltan datos", "Por favor, seleccione una fecha de nacimiento válida.")
                return

            meses_a_num_dict = {"Ene": "01", "Feb": "02", "Mar": "03", "Abr": "04", "May": "05", "Jun": "06", "Jul": "07", "Ago": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dic": "12"}
            fecha_nac_str = f"{anio}-{meses_a_num_dict[mes]}-{dia}"
            
            try:
                f_nac = datetime.strptime(fecha_nac_str, "%Y-%m-%d")
                hoy = datetime.today()
                edad_calculada = hoy.year - f_nac.year - ((hoy.month, hoy.day) < (f_nac.month, f_nac.day))
            except ValueError:
                messagebox.showerror("Error", "La fecha de nacimiento no es válida.")
                return

            
            hoy_str = datetime.today().strftime("%Y-%m-%d")

            nueva_usuaria = Usuaria(
                nombre = self.ent_nombre.get(),
                edad = edad_calculada,
                telefono = self.ent_telefono.get(),
                fecha_nacimiento = fecha_nac_str,
                lugar_nacimiento = self.ent_lugar.get(),
                escolaridad_id = self._texto_a_id(self.escolaridades_list, "escolaridad", self.opt_escolaridad.get(), "id_escolaridad"),
                ocupacion = self.ent_ocupacion.get(),
                estado_civil_id = self._texto_a_id(self.estados_civiles_list, "estado_civil", self.opt_civil.get(), "id_estado_civil"),
                sexo_id = self._texto_a_id(self.sexos_list, "sexo", self.opt_sexo.get(), "id_sexo"),
                lengua_indigena_id = self._texto_a_id(self.lenguas_indigenas_list, "lengua_indigena", self.opt_lengua.get(), "id_lengua_indigena"),
                padecimiento = ", ".join(self.padecimientos_seleccionados),
                servicio_immujer_id = 1 if self.var_immujer.get() == "Sí" else 2,
                servicio_immujer_fecha = self.ent_cuando.get() if self.var_immujer.get() == "Sí" else hoy_str, 
                terapia_tiempo = self.ent_tiempo.get() if self.var_terapia.get() == "Sí" else "", 
                terapia_lugar = self.ent_lugar_terapia.get() if self.var_terapia.get() == "Sí" else "",
                canalizada_por = self.opt_canalizada.get(),
                red_apoyo = self.ent_red_apoyo.get(),
                motivo_consulta = self.txt_motivo.get("0.0", "end").strip(),
                estatus_id = 1,
                id_usuaria = self.id_usuaria_editada if self.editando_usuaria else None 
            )

            if self.ent_agresor.get() != "" or self.ent_parentesco.get() != "" or self.ent_ocupacion_agresor.get() != "" or self.ent_edad_agresor.get() != "":
                self.datos_agresor = Agresor(
                    nombre_agresor = self.ent_agresor.get(),
                    parentesco_agresor = self.ent_parentesco.get(),
                    ocupacion_agresor = self.ent_ocupacion_agresor.get(),
                    edad_agresor = self.ent_edad_agresor.get(),
                    id_agresor = self.id_agresor_editado if self.editando_usuaria else None
                )
            
            if not self.editando_usuaria:
                confirmacion = messagebox.askyesno("Confirmar Registro", f"¿Está segura de que desea registrar a {self.ent_nombre.get()}?")
                if not confirmacion:
                    return
                res_usuaria = service_crear_usuaria(nueva_usuaria)
                if not res_usuaria.get("success"):
                    messagebox.showerror("Error al registrar", res_usuaria.get("error"))
                    return
                id_usuaria_creada = res_usuaria.get("id_usuaria")
            else:
                confirmacion = messagebox.askyesno("Confirmar Cambios", f"¿Guardar cambios hechos en la información de {self.ent_nombre.get()}?")
                if not confirmacion:
                    return
                res_actualizar_usuaria = service_actualizar_usuaria(nueva_usuaria)
                if not res_actualizar_usuaria.get("success"):
                    messagebox.showerror("Error al actualizar", res_actualizar_usuaria.get("error"))
                    return
            # Si hay información de direccion guardada
            if self.datos_domicilio:
                # Si no se esta editando una usuaria
                if not self.editando_usuaria:
                    res_direccion = service_crear_direccion(self.datos_domicilio)
                    if res_direccion.get("success"):
                        id_direccion_creada = res_direccion.get("id_direccion")
                        res_usuaria_direccion = service_crear_usuaria_direccion(id_usuaria_creada, id_direccion_creada)
                        if res_usuaria_direccion.get("success"):
                            pass
                        else:
                            messagebox.showwarning("Aviso", f"Usuaria creada, pero falló el domicilio: {res_usuaria_direccion.get('error')}")
                            return
                    else:
                        messagebox.showwarning("Aviso", f"Usuaria creada, pero falló el domicilio: {res_direccion.get('error')}")
                        return
                # Se esta editando una usuaria, pero no tiene direccion registrada
                elif self.id_direccion_editada == 0:
                    # Se registra una nueva direccion
                    res_direccion_usuaria_editada = service_crear_direccion(self.datos_domicilio)
                    if res_direccion_usuaria_editada.get("success"):
                        id_direccion_creada_usuaria_editada = res_direccion_usuaria_editada.get("id_direccion")
                        res_usuaria_direccion_usuaria_editada = service_crear_usuaria_direccion(self.id_usuaria_editada, id_direccion_creada_usuaria_editada)
                        if res_usuaria_direccion_usuaria_editada.get("success"):
                            pass
                        else:
                            messagebox.showwarning("Aviso", f"Usuaria actualizada, pero falló el domicilio: {res_usuaria_direccion.get('error')}")
                            return
                    else:
                        messagebox.showwarning("Aviso", f"Usuaria actualizada, pero falló el domicilio: {res_direccion.get('error')}")
                        return
                # Se esta editando una usuaria y tiene una direccion registrada
                else:
                    res_actualizar_direccion = service_actualizar_direccion(self.datos_domicilio)
                    if res_actualizar_direccion.get("success"):
                        pass
                    else:
                        messagebox.showwarning("Aviso", f"Usuaria actualizada, pero falló el domicilio: {res_direccion.get('error')}")
                        return
            
            #Hay información de agresor
            if self.datos_agresor:
                #No se está editando una usuaria
                if not self.editando_usuaria:
                    res_agresor = service_crear_y_vincular_agresor(id_usuaria_creada, self.datos_agresor)
                    if res_agresor.get("success"):
                        pass
                    else:
                        messagebox.showwarning("Aviso", f"Usuaria creada, pero falló al agregar agresor: {res_agresor.get('error')}")
                        return
                # Se esta editando una usuaria, pero no tiene agresor registrado
                elif self.id_agresor_editado == 0:
                    # Se registra un nuevo agresor
                    res_agresor_vincular = service_crear_y_vincular_agresor(self.id_usuaria_editada, self.datos_agresor)
                    if res_agresor_vincular.get("success"):
                        pass
                    else:
                        messagebox.showwarning("Aviso", f"Usuaria actualizada, pero falló al agregar agresor: {res_agresor.get('error')}")
                        return
                # Se esta editando una usuaria y tiene una agresor registrada
                else:
                    res_actualizar_agresor = service_actualizar_agresor(self.datos_agresor)
                    if res_actualizar_agresor.get("success"):
                        pass
                    else:
                        messagebox.showwarning("Aviso", f"Usuaria actualizada, pero falló el agresor: {res_agresor.get('error')}")
                        return
            if not self.editando_usuaria:
                messagebox.showinfo("Éxito", "¡Usuaria registrada correctamente!")
            else:
                messagebox.showinfo("Éxito", "¡Información de usuaria actualizada correctamente!")
                self.editando_usuaria = False
                self.refrescar_boton_registrar_editar()

            if self.on_actualizar:
                self.on_actualizar()
                
            self.limpiar_formulario()    
            self.volver_al_inicio()

    def limpiar_formulario(self):
        self.ent_nombre.delete(0, "end")
        self.opt_escolaridad.set("Ninguna")
        self.opt_dia.set("Día")
        self.opt_mes.set("Mes")
        self.opt_ano.set("Año")
        
        self.opt_sexo.set("Femenino")
        
        self.ent_lugar.delete(0, "end")
        
        self.opt_lengua.set("Ninguna") 
        
        self.ent_ocupacion.delete(0, "end")
        
        self.padecimientos_seleccionados = []
        self.btn_padecimiento.configure(text="📍 Seleccionar padecimientos...", text_color="gray", border_color="#D3D3D3", border_width=1)
        
        self.ent_telefono.delete(0, "end")
        
        self.datos_domicilio = None
        self.btn_domicilio.configure(text="📍 Ingresar Domicilio...", text_color="gray", border_color="#D3D3D3", border_width=1)
        
        self.opt_civil.set("Soltera")
        
        self.var_terapia.set("Sí")
        self.var_immujer.set("Sí")
        self.actualizar_campos_immujer()

        self.ent_cuando.delete(0, "end")
        self.ent_tipo_apoyo.delete(0, "end")
        self.ent_tiempo.delete(0, "end")
        self.ent_lugar_terapia.set("Público")

        self.var_terapia.set("No")
        self.var_immujer.set("No")
        self.actualizar_campos_immujer()
        
        self.opt_canalizada.set("Vicefiscalía")
        
        self.ent_red_apoyo.delete(0, "end")
        
        if hasattr(self, 'menus_familia'):
            for menu in self.menus_familia:
                menu.set("0")

        self.limpiar_entries_hijos(self.page2)
        
        self.txt_motivo.delete("0.0", "end")
        self.ent_agresor.delete(0, "end")
        self.ent_parentesco.delete(0, "end")
        self.ent_ocupacion_agresor.delete(0, "end")
        self.ent_edad_agresor.delete(0, "end")
        self.id_usuaria_editada = 0
        self.id_direccion_editada = 0
        self.id_agresor_editado = 0

    def limpiar_entries_hijos(self, parent):
        for widget in parent.winfo_children():
            if isinstance(widget, ctk.CTkEntry):
                widget.delete(0, "end")
            elif isinstance(widget, ctk.CTkFrame):
                self.limpiar_entries_hijos(widget)
                
    def abrir_modal_busqueda(self):
        modal = ctk.CTkToplevel(self)
        modal.title("Buscar Usuaria")
        modal.geometry("400x400") 
        modal.transient(self.winfo_toplevel())
        modal.grab_set()

        ctk.CTkLabel(modal, text="Seleccione una usuaria:", font=("Arial", 15, "bold"), text_color="#006B4D").pack(pady=(15, 5))

        scroll_frame = ctk.CTkScrollableFrame(modal, fg_color="white", border_width=1, border_color="#D3D3D3")
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.usuaria_seleccionada = ctk.StringVar(value="")

        usuarias_bd = service_obtener_usuarias()
        nombres_db = []
        for u in usuarias_bd:
            nombres_db.append(u.nombre + " - " + u.telefono)

        for nombre in nombres_db:
            rb = ctk.CTkRadioButton(
                scroll_frame, 
                text=nombre, 
                variable=self.usuaria_seleccionada, 
                value=nombre,
                fg_color="#7A1B6C",     
                hover_color="#E55A2B",  
                text_color="black"
            )
            rb.pack(anchor="w", pady=8, padx=10)

        def confirmar_seleccion():
            seleccion = self.usuaria_seleccionada.get()
            
            if seleccion != "":
                self.limpiar_formulario()
                modal.destroy()
                nombre_usuaria, telefono_usuaria = seleccion.split(" - ")
                datos_usuaria = service_obtener_usuaria_por_telefono(telefono_usuaria)
                self.id_usuaria_editada = datos_usuaria.id_usuaria
                usuaria_direccion = service_obtener_usuaria_direccion(datos_usuaria.id_usuaria)
                usuaria_agresor = service_obtener_usuaria_agresor(datos_usuaria.id_usuaria)
                datos_direccion = None
                datos_agresor = None

                if usuaria_direccion != None:
                    datos_direccion = service_obtener_direccion_por_id(usuaria_direccion["direccion_id"])
                    self.id_direccion_editada = datos_direccion.id_direccion
                
                if usuaria_agresor != None:
                    datos_agresor = service_obtener_agresor_por_id(usuaria_agresor["agresor_id"])
                    self.id_agresor_editado = datos_agresor.id_agresor
                
                llenar_campos_usuaria(datos_usuaria, datos_direccion, datos_agresor)
                messagebox.showinfo("Éxito", f"Datos de {nombre_usuaria} cargados.")
                self.editando_usuaria = True
                self.refrescar_boton_registrar_editar()
                self.btn_volver_inicio.grid()
                self.mostrar_pagina(self.page1)
            else:
                messagebox.showwarning("Atención", "Por favor, seleccione una usuaria de la lista antes de cargar.")

        def set_widget_text(widget, valor):
            valor = "" if valor is None else str(valor)
            if isinstance(widget, ctk.CTkEntry):
                widget.delete(0, "end")
                widget.insert(0, valor)
            elif isinstance(widget, ctk.CTkTextbox):
                widget.delete("1.0", "end")
                widget.insert("1.0", valor)
            elif isinstance(widget, ctk.CTkOptionMenu): 
                widget.set(valor)

        def llenar_campos_usuaria(usuaria: Usuaria, direccion: Direccion, agresor: Agresor):
            if direccion != None:
                self.datos_domicilio = direccion
                self.btn_domicilio.configure(text=" ✅ Domicilio guardado", text_color="black", border_color="#32CD32", border_width=2)
            
            if agresor != None:
                self.datos_agresor = agresor
                # Para agresor
                set_widget_text(self.ent_agresor, agresor.nombre_agresor)
                set_widget_text(self.ent_parentesco, agresor.parentesco_agresor)
                set_widget_text(self.ent_ocupacion_agresor, agresor.ocupacion_agresor)
                set_widget_text(self.ent_edad_agresor, agresor.edad_agresor)
            
            #if hasattr(self, 'menus_familia'):
            #    for menu in self.menus_familia:
            #        menu.set("1")
            #self.limpiar_entries_hijos(self.page2)
            familia_usuaria = ["1", "0", "2", "0", "1", "3"]
            if hasattr(self, 'menus_familia'):
                i = 0
                for menu in self.menus_familia:
                    menu.set(familia_usuaria[i])
                    i += 1

            self.var_immujer.set("Sí")
            self.var_terapia.set("Sí")
            self.actualizar_campos_immujer()
            set_widget_text(self.ent_nombre, usuaria.nombre)
            set_widget_text(self.ent_lugar, usuaria.lugar_nacimiento)
            set_widget_text(self.ent_ocupacion, usuaria.ocupacion)
            set_widget_text(self.ent_telefono, usuaria.telefono)
            set_widget_text(self.ent_cuando, usuaria.servicio_immujer_fecha)
            set_widget_text(self.ent_tipo_apoyo, "Psicológico")
            self.padecimientos_seleccionados = usuaria.padecimiento.split(", ")
            num_seleccionados = len(self.padecimientos_seleccionados)
            if num_seleccionados > 0:
                self.btn_padecimiento.configure(text=f" ✅ {num_seleccionados} seleccionados", text_color="black", border_color="#32CD32", border_width=2)
            set_widget_text(self.ent_tiempo, usuaria.terapia_tiempo)
            set_widget_text(self.ent_lugar_terapia, usuaria.terapia_lugar)
            set_widget_text(self.ent_red_apoyo, usuaria.red_apoyo)
            set_widget_text(self.txt_motivo, usuaria.motivo_consulta)


            self.opt_escolaridad.set(self._id_a_texto(self.escolaridades_list, "id_escolaridad", usuaria.escolaridad_id, "escolaridad"))
            anio_u, mes_u, dia_u = usuaria.fecha_nacimiento.split("-")
            self.opt_dia.set(dia_u)
            num_a_meses_dict = {"01":"Ene", "02":"Feb", "03":"Mar", "04":"Abr", "05":"May", "06":"Jun", "07":"Jul", "08":"Ago", "09":"Sep", "10":"Oct", "11":"Nov", "12":"Dic"}
            self.opt_mes.set(num_a_meses_dict[mes_u])
            self.opt_ano.set(anio_u)
            self.opt_sexo.set(self._id_a_texto(self.sexos_list, "id_sexo", usuaria.sexo_id, "sexo"))
            self.opt_lengua.set(self._id_a_texto(self.lenguas_indigenas_list, "id_lengua_indigena", usuaria.lengua_indigena_id, "lengua_indigena"))
            self.opt_civil.set(self._id_a_texto(self.estados_civiles_list, "id_estado_civil", usuaria.estado_civil_id, "estado_civil"))
            self.opt_canalizada.set(usuaria.canalizada_por)

            #self.padecimientos_seleccionados = []
            #self.btn_padecimiento.configure(text="📍 Seleccionar padecimientos...", text_color="gray", border_color="#D3D3D3", border_width=1)

        ctk.CTkButton(modal, text="Cargar Datos", command=confirmar_seleccion, fg_color="#FF6B35", text_color="white", font=("Arial", 15, "bold")).pack(pady=(10, 20))