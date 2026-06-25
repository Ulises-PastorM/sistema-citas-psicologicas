import customtkinter as ctk
import calendar
from services.citas_services import service_obtener_citas_usuarias
from datetime import date, timedelta, datetime


class CalendarioView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        hoy = date.today()
        self.anio_actual = hoy.year
        self.mes_actual = hoy.month
        self.fecha_seleccionada = hoy 
        self.filtro_actual = "Mes" 

        self.meses_nombres = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

        self.cargar_citas()

        self.lbl_titulo = ctk.CTkLabel(self, text="Calendario de Citas", font=("Arial", 22, "bold", "italic"), text_color="#006B4D")
        self.lbl_titulo.grid(row=0, column=0, pady=(0, 15), sticky="w")

        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=1, column=0, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(1, weight=1)

        self.card_calendario = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=15, border_width=1, border_color="#D3D3D3")
        self.card_calendario.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        self.cal_header = ctk.CTkFrame(self.card_calendario, fg_color="transparent")
        self.cal_header.pack(fill="x", pady=(20, 10), padx=20)
        
        btn_prev = ctk.CTkButton(self.cal_header, text="<", width=30, fg_color="transparent", text_color="#FF6B35", font=("Arial", 18, "bold"), hover_color="#F0F0F0", command=self.mes_anterior)
        btn_prev.pack(side="left")
        
        self.lbl_mes = ctk.CTkLabel(self.cal_header, text="", font=("Arial", 18, "bold"), text_color="#7A1B6C")
        self.lbl_mes.pack(side="left", expand=True)
        
        btn_next = ctk.CTkButton(self.cal_header, text=">", width=30, fg_color="transparent", text_color="#FF6B35", font=("Arial", 18, "bold"), hover_color="#F0F0F0", command=self.mes_siguiente)
        btn_next.pack(side="right")

        self.cal_grid = ctk.CTkFrame(self.card_calendario, fg_color="transparent")
        self.cal_grid.pack(expand=True, fill="both", padx=20, pady=(0, 20))

        self.card_citas = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=15, border_width=1, border_color="#D3D3D3")
        self.card_citas.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        lbl_citas_titulo = ctk.CTkLabel(self.card_citas, text="🔔 Próximas Citas", font=("Arial", 18, "bold"), text_color="#7A1B6C")
        lbl_citas_titulo.pack(pady=(20, 10))

        self.tabs_frame = ctk.CTkFrame(self.card_citas, fg_color="transparent")
        self.tabs_frame.pack(fill="x", padx=30)
        self.tabs_frame.grid_columnconfigure((0,1,2), weight=1)

        btn_style = {"fg_color": "transparent", "font": ("Arial", 12, "bold", "italic"), "hover_color": "#F0F0F0"}

        self.btn_filtro_dia = ctk.CTkButton(self.tabs_frame, text="Día", command=lambda: self.cambiar_filtro("Día"), **btn_style)
        self.btn_filtro_dia.grid(row=0, column=0, sticky="ew")

        self.btn_filtro_semana = ctk.CTkButton(self.tabs_frame, text="Semana", command=lambda: self.cambiar_filtro("Semana"), **btn_style)
        self.btn_filtro_semana.grid(row=0, column=1, sticky="ew")

        self.btn_filtro_mes = ctk.CTkButton(self.tabs_frame, text="Mes", command=lambda: self.cambiar_filtro("Mes"), **btn_style)
        self.btn_filtro_mes.grid(row=0, column=2, sticky="ew")
        
        ctk.CTkFrame(self.card_citas, height=2, fg_color="#FF6B35").pack(fill="x", padx=15, pady=(5, 15))

        self.scroll_citas = ctk.CTkScrollableFrame(self.card_citas, fg_color="transparent", width=300, height=350)
        self.scroll_citas.pack(fill="both", expand=True, padx=10, pady=(0, 15))

        self.renderizar_calendario()
        self.cambiar_filtro("Mes") 

    def mes_anterior(self):
        if self.mes_actual == 1:
            self.mes_actual = 12
            self.anio_actual -= 1
        else:
            self.mes_actual -= 1
        self.renderizar_calendario()
        self.actualizar_citas()

    def mes_siguiente(self):
        if self.mes_actual == 12:
            self.mes_actual = 1
            self.anio_actual += 1
        else:
            self.mes_actual += 1
        self.renderizar_calendario()
        self.actualizar_citas()

    def seleccionar_dia(self, dia):
        self.fecha_seleccionada = date(self.anio_actual, self.mes_actual, dia)
        self.renderizar_calendario() 
        self.actualizar_citas()   

    def renderizar_calendario(self):
        for widget in self.cal_grid.winfo_children():
            widget.destroy()

        self.lbl_mes.configure(text=f"{self.meses_nombres[self.mes_actual]} {self.anio_actual}")

        dias_semana = ["Dom", "Lun", "Mar", "Mié", "Jue", "Vie", "Sáb"]
        for i, dia in enumerate(dias_semana):
            self.cal_grid.grid_columnconfigure(i, weight=1)
            ctk.CTkLabel(self.cal_grid, text=dia, font=("Arial", 13), text_color="gray").grid(row=0, column=i, pady=10)


        primer_dia_mes_weekday, num_dias = calendar.monthrange(self.anio_actual, self.mes_actual)
        columna_inicio = (primer_dia_mes_weekday + 1) % 7 

        row, col = 1, columna_inicio

        for day in range(1, num_dias + 1):
            fecha_actual_loop = date(self.anio_actual, self.mes_actual, day)
            
            color_fondo = "transparent"
            color_texto = "black"
            borde = 0

            if fecha_actual_loop in self.db_citas:
                color_fondo = self.db_citas[fecha_actual_loop][0]["color"]
                color_texto = "white"

            if fecha_actual_loop == self.fecha_seleccionada:
                if color_fondo == "transparent":
                    color_fondo = "#E0E0E0" 
                borde = 2

            btn_dia = ctk.CTkButton(
                self.cal_grid, text=str(day), width=32, height=32, corner_radius=16, 
                fg_color=color_fondo, text_color=color_texto, border_width=borde, border_color="#7A1B6C",
                font=("Arial", 13), hover_color="#D3D3D3", command=lambda d=day: self.seleccionar_dia(d)
            )
            btn_dia.grid(row=row, column=col, pady=8, padx=5)
            
            col += 1
            if col > 6:
                col = 0
                row += 1

    def cambiar_filtro(self, filtro):
        self.filtro_actual = filtro
        
        self.btn_filtro_dia.configure(text_color="gray")
        self.btn_filtro_semana.configure(text_color="gray")
        self.btn_filtro_mes.configure(text_color="gray")
        
        if filtro == "Día": self.btn_filtro_dia.configure(text_color="#7A1B6C")
        elif filtro == "Semana": self.btn_filtro_semana.configure(text_color="#7A1B6C")
        elif filtro == "Mes": self.btn_filtro_mes.configure(text_color="#7A1B6C")

        self.actualizar_citas()

    def actualizar_citas(self):
        for widget in self.scroll_citas.winfo_children():
            widget.destroy()

        citas_a_mostrar = []

        for fecha_cita, lista_citas in self.db_citas.items():
            mostrar = False
            
            if self.filtro_actual == "Día":
                if fecha_cita == self.fecha_seleccionada:
                    mostrar = True
                    
            elif self.filtro_actual == "Semana":
                fecha_fin_semana = self.fecha_seleccionada + timedelta(days=6)
                if self.fecha_seleccionada <= fecha_cita <= fecha_fin_semana:
                    mostrar = True
                    
            elif self.filtro_actual == "Mes":
                if fecha_cita.month == self.mes_actual and fecha_cita.year == self.anio_actual:
                    mostrar = True

            if mostrar:
                for cita in lista_citas:
                    citas_a_mostrar.append((fecha_cita, cita))

        citas_a_mostrar.sort(key=lambda x: x[0])

        if not citas_a_mostrar:
            ctk.CTkLabel(self.scroll_citas, text="No hay citas en este periodo.", text_color="gray", font=("Arial", 12, "italic")).pack(pady=20)
            return

        for fecha_cita, cita in citas_a_mostrar:
            dia_str = str(fecha_cita.day)
            mes_str = self.meses_nombres[fecha_cita.month][:3] 
            self.crear_tarjeta_cita(self.scroll_citas, dia_str, mes_str, cita["hora"], cita["nombre"], cita["color"], cita["estatus"])

    def crear_tarjeta_cita(self, master, dia, mes, hora, nombre, color_borde, estatus):
        card = ctk.CTkFrame(master, fg_color="white", border_width=2, border_color="#B4B4B4", corner_radius=8, height=60)
        card.pack(fill="x", padx=(5, 30), pady=5)
        card.pack_propagate(False) 
        
        borde = ctk.CTkFrame(card, width=6, fg_color=color_borde, corner_radius=6)
        borde.pack(side="left", fill="y", pady=4, padx=4)
        
        fecha_frame = ctk.CTkFrame(card, fg_color="transparent", width=45)
        fecha_frame.pack(side="left", padx=10, pady=3)
        ctk.CTkLabel(fecha_frame, text=dia, font=("Arial", 14, "bold"), text_color="gray", height=20).pack(pady=(6, 0))
        ctk.CTkLabel(fecha_frame, text=mes, font=("Arial", 11), text_color="gray", height=15).pack(pady=(0, 4))

        info_frame = ctk.CTkFrame(card, fg_color="transparent")

        info_frame.pack(side="left", fill="both", expand=True, padx=5, pady=3)
        
        top_info = ctk.CTkFrame(info_frame, fg_color="transparent")
        top_info.pack(fill="x", pady=(8, 0))
        ctk.CTkLabel(top_info, text=f"🕒 {hora}", font=("Arial", 11), text_color="gray", height=15).pack(side="left")
        
        badge = ctk.CTkLabel(top_info, text=f" {estatus} ", fg_color=color_borde, text_color="white", font=("Arial", 10, "bold"), corner_radius=10, height=18)
        badge.pack(side="right") 

        ctk.CTkLabel(info_frame, text=nombre, font=("Arial", 13, "bold"), text_color="black", height=20).pack(side="left", anchor="w", pady=(2, 0))
        
    def cargar_citas(self):
        self.db_citas = {}
        citas_raw = service_obtener_citas_usuarias()

        colores = {
            "Activa": "#32CD32",       
            "Completada": "#7A1B6C",   
            "Cancelada": "#FF6B35"     
        }

        for cita in citas_raw:
            nombre = cita[0]
            fecha_str = cita[1]
            hora = cita[3]
            estatus = cita[4]
            
            if estatus == "Cancelada":
                continue

            try:
                fecha_obj = datetime.strptime(fecha_str, "%Y-%m-%d").date()
            except ValueError:
                continue 

            cita_dict = {
                "hora": hora,
                "nombre": nombre,
                "color": colores.get(estatus, "#B4B4B4"), 
                "estatus": estatus
            }

            if fecha_obj not in self.db_citas:
                self.db_citas[fecha_obj] = []
            
            self.db_citas[fecha_obj].append(cita_dict)
    
    def refrescar_datos(self):
        self.cargar_citas()
        self.renderizar_calendario()
        self.actualizar_citas()