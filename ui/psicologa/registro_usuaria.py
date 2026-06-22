import customtkinter as ctk

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

        self.card_frame = ctk.CTkScrollableFrame(self, fg_color="#F4F4F4", corner_radius=15)
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
        
        f_esc, self.opt_escolaridad = self.crear_campo_opciones(self.page1, "Escolaridad:", ["Primaria", "Secundaria", "Preparatoria", "Universidad"])
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
        self.ent_sexo_otra = ctk.CTkEntry(f_sex, placeholder_text="Especifique cuál...", **self.entry_style)
        def verificar_sexo(valor_seleccionado):
            if valor_seleccionado == "Otro":
                self.ent_sexo_otra.pack(fill="x", expand=True, pady=(5, 0))
            else:
                self.ent_sexo_otra.pack_forget()
                self.ent_sexo_otra.delete(0, "end")
                
        self.opt_sexo.configure(command=verificar_sexo)
        f_sex.grid(row=2, column=1, sticky="ew", padx=(10, 0), pady=(0, 12))
        
        f_lug, self.ent_lugar = self.crear_campo_entrada(self.page1, "Lugar de nacimiento:")
        f_lug.grid(row=3, column=0, sticky="ew", padx=(0, 10), pady=(0, 12))
        
        f_len, self.opt_lengua = self.crear_campo_opciones(self.page1, "Lengua indígena:", ["Mixteco", "Ninguna", "Otra"])
        
        self.ent_lengua_otra = ctk.CTkEntry(f_len, placeholder_text="Especifique cuál...", **self.entry_style)
        
        def verificar_lengua(valor_seleccionado):
            if valor_seleccionado == "Otra":
                self.ent_lengua_otra.pack(fill="x", expand=True, pady=(5, 0))
            else:
                self.ent_lengua_otra.pack_forget()
                self.ent_lengua_otra.delete(0, "end")
                
        self.opt_lengua.configure(command=verificar_lengua)
        
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

        scroll_pad = ctk.CTkScrollableFrame(modal, fg_color="transparent")
        scroll_pad.pack(fill="both", expand=True, padx=30, pady=(0, 10))

        checkbox_vars = {}

        ent_otro_pad = ctk.CTkEntry(scroll_pad, placeholder_text="Especifique el padecimiento...", **self.entry_style)

        def verificar_otro():
            if checkbox_vars["Otro"].get() == "Otro":
                ent_otro_pad.pack(fill="x", padx=25, pady=(0, 5)) 
            else:
                ent_otro_pad.pack_forget()

        for pad in self.lista_padecimientos:
            valor_inicial = pad if pad in self.padecimientos_seleccionados else ""
            var = ctk.StringVar(value=valor_inicial)
            checkbox_vars[pad] = var
            
            if pad == "Otro":
                cb = ctk.CTkCheckBox(scroll_pad, text=pad, variable=var, onvalue=pad, offvalue="", fg_color="#FF6B35", hover_color="#E55A2B", text_color="black", command=verificar_otro)
            else:
                cb = ctk.CTkCheckBox(scroll_pad, text=pad, variable=var, onvalue=pad, offvalue="", fg_color="#FF6B35", hover_color="#E55A2B", text_color="black")
            cb.pack(anchor="w", pady=5)

            if pad == "Otro" and valor_inicial == "Otro":
                ent_otro_pad.pack(fill="x", padx=25, pady=(0, 5))
                ent_otro_pad.insert(0, self.padecimiento_otro_texto)

        def guardar_padecimientos():
            self.padecimientos_seleccionados = [var.get() for var in checkbox_vars.values() if var.get() != ""]
            
            if "Otro" in self.padecimientos_seleccionados:
                self.padecimiento_otro_texto = ent_otro_pad.get()
            else:
                self.padecimiento_otro_texto = "" 
                
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
        modal.geometry("400x350")
        modal.resizable(False, False)
        
        modal.transient(self.winfo_toplevel())
        modal.grab_set()

        ctk.CTkLabel(modal, text="🏠 Dirección y Estatus", font=("Arial", 16, "bold"), text_color="#006B4D").pack(pady=(20, 15))

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
            ent_colonia.insert(0, self.datos_domicilio.get("colonia", ""))
            ent_municipio.insert(0, self.datos_domicilio.get("municipio", ""))
            opt_estatus.set(self.datos_domicilio.get("estatus", "Propio"))

        def guardar_datos():
            self.datos_domicilio = {
                "colonia": ent_colonia.get(),
                "municipio": ent_municipio.get(),
                "estatus": opt_estatus.get()
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
        
        ctk.CTkLabel(tabla_frame, text="Mujeres:", text_color="gray").grid(row=1, column=0, sticky="e", padx=5)
        for i in range(1, 4): 
            ctk.CTkEntry(tabla_frame, height=30, fg_color="white", text_color="black", validate="key", validatecommand=self.vcmd_numeros).grid(row=1, column=i, padx=5, pady=2, sticky="ew")
        
        ctk.CTkLabel(tabla_frame, text="Hombres:", text_color="gray").grid(row=2, column=0, sticky="e", padx=5)
        for i in range(1, 4): 
            ctk.CTkEntry(tabla_frame, height=30, fg_color="white", text_color="black", validate="key", validatecommand=self.vcmd_numeros).grid(row=2, column=i, padx=5, pady=2, sticky="ew")

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
        self.ent_canalizada_otra = ctk.CTkEntry(f_can, placeholder_text="Especifique cuál...", **self.entry_style)
        def verificar_can(valor_seleccionado):
            if valor_seleccionado == "Otra":
                self.ent_canalizada_otra.pack(fill="x", expand=True, pady=(5, 0))
            else:
                self.ent_canalizada_otra.pack_forget()
                self.ent_canalizada_otra.delete(0, "end")
                
        self.opt_canalizada.configure(command=verificar_can)
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
        
        btn_submit = ctk.CTkButton(self.page3, text="+ Registrar Usuaria", fg_color="#FF6B35", text_color="white", font=("Arial", 15, "bold"), height=35, corner_radius=8)
        btn_submit.grid(row=4, column=1, sticky="e", pady=(20, 0))