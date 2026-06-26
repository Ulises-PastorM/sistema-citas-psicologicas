import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from models.usuaria_model import Usuaria
from models.direccion_model import Direccion
from services.usuarias_services import service_crear_usuaria, service_crear_usuaria_direccion
from services.direcciones_services import service_crear_direccion

class RegistroUsuariaView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.datos_domicilio = {}
        self.padecimientos_seleccionados = [] 
        
        self.lista_padecimientos = [
            "Violencia física", "Violencia psicológica", "Violencia sexual", 
            "Violencia económica", "Violencia patrimonial", "Violencia vicaria", 
            "Violencia digital", "Pensión alimenticia", "Guardia y custodia", "Otro"
        ]

        self.lbl_titulo = ctk.CTkLabel(self, text="Registro de Usuaria para Atención Psicológica", font=("Arial", 20, "bold", "italic"), text_color="#006B4D")
        self.lbl_titulo.grid(row=0, column=0, pady=(0, 10), sticky="w")

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
            "font": ("Arial", 18, "bold"), 
            "width": 40, 
            "height": 35, 
            "corner_radius": 8
        }

        self.vcmd_numeros = (self.register(self.solo_numeros), '%P')

        self.crear_pagina_1()
        self.crear_pagina_2()
        self.crear_pagina_3()

        self.mostrar_pagina(self.page1)

    def solo_numeros(self, texto_propuesto):
        return texto_propuesto.isdigit() or texto_propuesto == ""

    def mostrar_pagina(self, pagina):
        # Ocultamos todas las páginas de la cuadrícula
        if hasattr(self, 'page1'): self.page1.grid_forget()
        if hasattr(self, 'page2'): self.page2.grid_forget()
        if hasattr(self, 'page3'): self.page3.grid_forget()
        
        # Solo volvemos a dibujar la que queremos ver
        pagina.grid(row=0, column=0, sticky="nsew", padx=30, pady=15)

    def crear_campo_entrada(self, parent, texto_label, ancho=None, validacion=None):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        ctk.CTkLabel(frame, text=texto_label, text_color="#555555", font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 2))
        
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
        ctk.CTkLabel(frame, text=texto_label, text_color="#555555", font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 2))
        
        menu = ctk.CTkOptionMenu(frame, values=opciones, **self.option_style)
        menu.pack(fill="x", expand=True)
        return frame, menu

    def crear_campo_boton(self, parent, texto_label, texto_boton, comando):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        ctk.CTkLabel(frame, text=texto_label, text_color="#555555", font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 2))
        
        btn = ctk.CTkButton(frame, text=texto_boton, command=comando,
                            fg_color="white", text_color="gray", hover_color="#F0F0F0",
                            border_width=1, border_color="#D3D3D3",
                            corner_radius=8, height=35, anchor="w")
        btn.pack(fill="x", expand=True)
        return frame, btn

    def crear_pagina_1(self):
        self.page1 = ctk.CTkFrame(self.card_frame, fg_color="transparent")
        self.page1.grid(row=0, column=0, sticky="nsew", padx=30, pady=15)
        self.page1.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(self.page1, text="Registrar Usuaria", font=("Arial", 14, "bold", "italic"), text_color="#006B4D").grid(row=0, column=0, sticky="w", pady=(0, 10))

        f_nom, self.ent_nombre = self.crear_campo_entrada(self.page1, "Nombre completo:")
        f_nom.grid(row=1, column=0, sticky="ew", padx=(0, 10), pady=(0, 12))
        
        f_esc, self.opt_escolaridad = self.crear_campo_opciones(self.page1, "Escolaridad:", ["Ninguna", "Primaria", "Secundaria", "Bachillerato", "Licenciatura", "Posgrado"])
        f_esc.grid(row=1, column=1, sticky="ew", padx=(10, 0), pady=(0, 12))
        
        f_fec = ctk.CTkFrame(self.page1, fg_color="transparent")
        f_fec.grid(row=2, column=0, sticky="ew", padx=(0, 10), pady=(0, 12))
        ctk.CTkLabel(f_fec, text="Fecha de nacimiento 📅:", text_color="#555555", font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 2))
        
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
        
        f_sex, self.opt_sexo = self.crear_campo_opciones(self.page1, "Sexo:", ["Femenino", "Masculino", "Otro"])
        f_sex.grid(row=2, column=1, sticky="ew", padx=(10, 0), pady=(0, 12))
        
        f_lug, self.ent_lugar = self.crear_campo_entrada(self.page1, "Lugar de nacimiento:")
        f_lug.grid(row=3, column=0, sticky="ew", padx=(0, 10), pady=(0, 12))
        
        f_len, self.opt_lengua = self.crear_campo_opciones(self.page1, "Lengua indígena:", ["Ninguna", "Mixteco", "Zapoteco", "Mazateco", "Otra"])
        f_len.grid(row=3, column=1, sticky="ew", padx=(10, 0), pady=(0, 12))

        f_ocu, self.ent_ocupacion = self.crear_campo_entrada(self.page1, "Ocupación:")
        f_ocu.grid(row=4, column=0, sticky="ew", padx=(0, 10), pady=(0, 12))
        
        f_pad, self.btn_padecimiento = self.crear_campo_boton(self.page1, "Padecimiento(s):", "📍 Seleccionar padecimientos...", self.abrir_modal_padecimientos)
        f_pad.grid(row=4, column=1, sticky="ew", padx=(10, 0), pady=(0, 12))
        
        f_tel, self.ent_telefono = self.crear_campo_entrada(self.page1, "Número de teléfono:", validacion=self.vcmd_numeros)
        f_tel.grid(row=5, column=0, sticky="ew", padx=(0, 10), pady=(0, 12))
        
        f_dom, self.btn_domicilio = self.crear_campo_boton(self.page1, "Domicilio:", "📍 Ingresar Domicilio...", self.abrir_modal_domicilio)
        f_dom.grid(row=5, column=1, sticky="ew", padx=(10, 0), pady=(0, 12))
        
        f_civ, self.opt_civil = self.crear_campo_opciones(self.page1, "Estado civil:", ["Soltera", "Casada", "Divorciada", "Viuda"])
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

        ctk.CTkLabel(modal, text="⚕️ Seleccione los padecimientos", font=("Arial", 16, "bold"), text_color="#006B4D").pack(pady=(20, 10))

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

        ctk.CTkButton(modal, text="Guardar Selección", command=guardar_padecimientos, fg_color="#FF6B35", text_color="white", font=("Arial", 14, "bold"), corner_radius=8, height=35).pack(pady=(0, 20))
        
    def abrir_modal_domicilio(self):
        modal = ctk.CTkToplevel(self)
        modal.title("Detalles del Domicilio")
        modal.geometry("400x450")
        modal.resizable(False, False)
        
        modal.transient(self.winfo_toplevel())
        modal.grab_set()

        ctk.CTkLabel(modal, text="🏠 Dirección y Estatus", font=("Arial", 16, "bold"), text_color="#006B4D").pack(pady=(20, 15))

        ctk.CTkLabel(modal, text="Calle y Número:", text_color="#555555", font=("Arial", 12, "bold")).pack(anchor="w", padx=30)
        ent_calle = ctk.CTkEntry(modal, **self.entry_style)
        ent_calle.pack(fill="x", padx=30, pady=(0, 15))

        ctk.CTkLabel(modal, text="Colonia ó Agencia:", text_color="#555555", font=("Arial", 12, "bold")).pack(anchor="w", padx=30)
        ent_colonia = ctk.CTkEntry(modal, **self.entry_style)
        ent_colonia.pack(fill="x", padx=30, pady=(0, 15))

        ctk.CTkLabel(modal, text="Municipio:", text_color="#555555", font=("Arial", 12, "bold")).pack(anchor="w", padx=30)
        ent_municipio = ctk.CTkEntry(modal, **self.entry_style)
        ent_municipio.pack(fill="x", padx=30, pady=(0, 15))

        ctk.CTkLabel(modal, text="Estatus de su domicilio:", text_color="#555555", font=("Arial", 12, "bold")).pack(anchor="w", padx=30)
        opt_estatus = ctk.CTkOptionMenu(modal, values=["Propio", "Rentado", "Prestado"], **self.option_style)
        opt_estatus.pack(fill="x", padx=30, pady=(0, 25))

        if self.datos_domicilio:
            ent_calle.insert(0, self.datos_domicilio.get("calle_numero", ""))
            ent_colonia.insert(0, self.datos_domicilio.get("colonia", ""))
            ent_municipio.insert(0, self.datos_domicilio.get("municipio", ""))
            opt_estatus.set(self.datos_domicilio.get("estatus", "Propio"))

        def guardar_datos():
            estatus_map = {"Propio": 1, "Rentado": 2, "Prestado": 3}
            
            self.datos_domicilio = {
                "calle_numero": ent_calle.get(),
                "colonia": ent_colonia.get(),
                "municipio": ent_municipio.get(),
                "estatus": opt_estatus.get(),
                "estatus_id": estatus_map.get(opt_estatus.get(), 1)
            }
            self.btn_domicilio.configure(text=" ✅ Domicilio guardado", text_color="black", border_color="#32CD32", border_width=2)
            modal.destroy()

        btn_guardar = ctk.CTkButton(modal, text="Guardar Datos", command=guardar_datos, fg_color="#FF6B35", text_color="white", font=("Arial", 14, "bold"), corner_radius=8, height=35)
        btn_guardar.pack(pady=(0, 20))

    def crear_pagina_2(self):
        self.page2 = ctk.CTkFrame(self.card_frame, fg_color="transparent")
        self.page2.grid(row=0, column=0, sticky="nsew", padx=30, pady=15)
        self.page2.grid_columnconfigure((0, 1, 2, 3), weight=1)

        ctk.CTkLabel(self.page2, text="Integrantes de la familia", font=("Arial", 14, "bold", "italic"), text_color="#006B4D").grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 10))

        tabla_frame = ctk.CTkFrame(self.page2, fg_color="transparent")
        tabla_frame.grid(row=1, column=0, columnspan=4, sticky="ew", pady=(0, 10))
        for i in range(4): tabla_frame.grid_columnconfigure(i, weight=1)

        headers = ["", "Edad de:\n0-14", "Edad de:\n14-18", "Mayor de\n18"]
        for i, text in enumerate(headers):
            ctk.CTkLabel(tabla_frame, text=text, text_color="gray", font=("Arial", 11)).grid(row=0, column=i, pady=2)
        
        opciones_numeros = [str(n) for n in range(16)]
        
        self.menus_familia = [] 

        ctk.CTkLabel(tabla_frame, text="Mujeres:", text_color="gray").grid(row=1, column=0, sticky="e", padx=5)
        for i in range(1, 4): 
            menu = ctk.CTkOptionMenu(tabla_frame, values=opciones_numeros, **self.option_style)
            menu.set("0") 
            menu.grid(row=1, column=i, padx=5, pady=2, sticky="ew")
            self.menus_familia.append(menu)
        
        ctk.CTkLabel(tabla_frame, text="Hombres:", text_color="gray").grid(row=2, column=0, sticky="e", padx=5)
        for i in range(1, 4): 
            menu = ctk.CTkOptionMenu(tabla_frame, values=opciones_numeros, **self.option_style)
            menu.set("0") 
            menu.grid(row=2, column=i, padx=5, pady=2, sticky="ew")
            self.menus_familia.append(menu)
            
        ctk.CTkFrame(self.page2, height=2, fg_color="#D3D3D3").grid(row=2, column=0, columnspan=4, sticky="ew", pady=10)

        ctk.CTkLabel(self.page2, text="Anteriormente\n¿Acudió a INMUJER?", text_color="gray").grid(row=3, column=0, sticky="e", padx=5)
        self.var_inmujer = ctk.StringVar(value="No")
        ctk.CTkRadioButton(self.page2, text="Sí", variable=self.var_inmujer, value="Sí", radiobutton_width=15, radiobutton_height=15).grid(row=3, column=1, sticky="w")
        ctk.CTkRadioButton(self.page2, text="No", variable=self.var_inmujer, value="No", radiobutton_width=15, radiobutton_height=15).grid(row=3, column=1, sticky="e")
        
        f_cua, self.ent_cuando = self.crear_campo_entrada(self.page2, "¿Cuándo?")
        f_cua.grid(row=3, column=2, padx=5, sticky="ew", pady=(0, 10))
        
        f_tip, self.ent_tipo_apoyo = self.crear_campo_entrada(self.page2, "Tipo de apoyo/Asesoría:")
        f_tip.grid(row=3, column=3, padx=5, sticky="ew", pady=(0, 10))

        ctk.CTkLabel(self.page2, text="Anteriormente\n¿Ha recibido terapia?", text_color="gray").grid(row=4, column=0, sticky="e", padx=5, pady=10)
        self.var_terapia = ctk.StringVar(value="No")
        ctk.CTkRadioButton(self.page2, text="Sí", variable=self.var_terapia, value="Sí", radiobutton_width=15, radiobutton_height=15).grid(row=4, column=1, sticky="w")
        ctk.CTkRadioButton(self.page2, text="No", variable=self.var_terapia, value="No", radiobutton_width=15, radiobutton_height=15).grid(row=4, column=1, sticky="e")
        
        f_tie, self.ent_tiempo = self.crear_campo_entrada(self.page2, "Tiempo:")
        f_tie.grid(row=4, column=2, padx=5, sticky="ew", pady=(0, 10))
        
        f_lug_terapia, self.ent_lugar_terapia = self.crear_campo_entrada(self.page2, "Lugar:")
        f_lug_terapia.grid(row=4, column=3, padx=5, sticky="ew", pady=(0, 10))

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
        ctk.CTkLabel(f_motivo, text="Motivo de la consulta:", text_color="#555555", font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 2))
        
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
        
        btn_prev = ctk.CTkButton(self.page3, text="🡨", command=lambda: self.mostrar_pagina(self.page2), **self.btn_nav_style)
        btn_prev.grid(row=4, column=0, sticky="w", pady=(20, 0))

        btn_submit = ctk.CTkButton(self.page3, text="+ Registrar Usuaria", fg_color="#FF6B35", text_color="white", font=("Arial", 15, "bold"), height=35, corner_radius=8, command=self.guardar_registro)
        btn_submit.grid(row=4, column=1, sticky="e", pady=(20, 0))
        
        
    def guardar_registro(self):
            dia = self.opt_dia.get()
            mes = self.opt_mes.get()
            anio = self.opt_ano.get()
            
            if dia == "Día" or mes == "Mes" or anio == "Año":
                messagebox.showwarning("Faltan datos", "Por favor, seleccione una fecha de nacimiento válida.")
                return

            meses_dict = {"Ene": "01", "Feb": "02", "Mar": "03", "Abr": "04", "May": "05", "Jun": "06", "Jul": "07", "Ago": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dic": "12"}
            fecha_nac_str = f"{anio}-{meses_dict[mes]}-{dia}"
            
            try:
                f_nac = datetime.strptime(fecha_nac_str, "%Y-%m-%d")
                hoy = datetime.today()
                edad_calculada = hoy.year - f_nac.year - ((hoy.month, hoy.day) < (f_nac.month, f_nac.day))
            except ValueError:
                messagebox.showerror("Error", "La fecha de nacimiento no es válida.")
                return

            map_escolaridad = {"Ninguna": 1, "Primaria": 2, "Secundaria": 3, "Bachillerato": 4, "Licenciatura": 5, "Posgrado": 6}
            map_sexo = {"Femenino": 1, "Masculino": 2, "Otro": 3}
            map_lengua = {"Ninguna": 1, "Mixteco": 2, "Zapoteco": 3, "Mazateco": 4, "Otra": 5}
            map_civil = {"Soltera": 1, "Casada": 2, "Divorciada": 3, "Viuda": 4, "Union Libre": 5}
            
            hoy_str = datetime.today().strftime("%Y-%m-%d")

            nueva_usuaria = Usuaria(
                nombre = self.ent_nombre.get(),
                edad = edad_calculada,
                telefono = self.ent_telefono.get(),
                fecha_nacimiento = fecha_nac_str,
                lugar_nacimiento = self.ent_lugar.get(),
                escolaridad_id = map_escolaridad.get(self.opt_escolaridad.get(), 1),
                ocupacion = self.ent_ocupacion.get(),
                estado_civil_id = map_civil.get(self.opt_civil.get(), 1),
                sexo_id = map_sexo.get(self.opt_sexo.get(), 1),
                lengua_indigena_id = map_lengua.get(self.opt_lengua.get(), 1),
                padecimiento = ", ".join(self.padecimientos_seleccionados),
                servicio_immujer_id = 1 if self.var_inmujer.get() == "Sí" else 2,
                servicio_immujer_fecha = hoy_str, 
                terapia_tiempo = "6 meses", 
                terapia_lugar = "Centro de Atención IMMUJER",
                canalizada_por = self.opt_canalizada.get(),
                red_apoyo = self.ent_red_apoyo.get(),
                motivo_consulta = self.txt_motivo.get("0.0", "end").strip(),
                estatus_id = 1 
            )

            confirmacion = messagebox.askyesno("Confirmar Registro", f"¿Está segura de que desea registrar a {self.ent_nombre.get()}?")
            
            if not confirmacion:
                return
            
            res_usuaria = service_crear_usuaria(nueva_usuaria)
            
            if not res_usuaria.get("success"):
                messagebox.showerror("Error al registrar", res_usuaria.get("error"))
                return
            
            id_usuaria_creada = res_usuaria.get("id_usuaria")

            if self.datos_domicilio:
                nueva_direccion = Direccion(
                    calle_numero = self.datos_domicilio.get("calle_numero", ""),
                    colonia = self.datos_domicilio.get("colonia", ""),
                    municipio = self.datos_domicilio.get("municipio", ""),
                    domicilio_estatus_id = self.datos_domicilio.get("estatus_id", 1)
                )
                res_direccion = service_crear_direccion(nueva_direccion)
                
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

            messagebox.showinfo("Éxito", "¡Usuaria registrada correctamente!")
            self.limpiar_formulario()    
            self.mostrar_pagina(self.page1)
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
        
        self.datos_domicilio = {}
        self.btn_domicilio.configure(text="📍 Ingresar Domicilio...", text_color="gray", border_color="#D3D3D3", border_width=1)
        
        self.opt_civil.set("Soltera")
        
        self.var_inmujer.set("No")
        self.ent_cuando.delete(0, "end")
        self.ent_tipo_apoyo.delete(0, "end")
        
        self.var_terapia.set("No")
        self.ent_tiempo.delete(0, "end")
        self.ent_lugar_terapia.delete(0, "end")
        
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

    def limpiar_entries_hijos(self, parent):
        for widget in parent.winfo_children():
            if isinstance(widget, ctk.CTkEntry):
                widget.delete(0, "end")
            elif isinstance(widget, ctk.CTkFrame):
                self.limpiar_entries_hijos(widget)