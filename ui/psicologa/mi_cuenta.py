import customtkinter as ctk

class MiCuentaView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        titulos_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        titulos_frame.pack(side="left")
        ctk.CTkLabel(titulos_frame, text="Mi Cuenta", font=("Arial", 22, "bold"), text_color="#006B4D").pack(anchor="w")

        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.grid(row=1, column=0, sticky="nsew")
        main_container.grid_columnconfigure(0, weight=1, uniform="col")
        main_container.grid_columnconfigure(1, weight=1, uniform="col")
        main_container.grid_rowconfigure(0, weight=1)


        card_info = ctk.CTkFrame(main_container, fg_color="white", corner_radius=15, border_width=1, border_color="#E0E0E0")
        card_info.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        ctk.CTkLabel(card_info, text="Información Personal", font=("Arial", 16, "bold"), text_color="#006B4D").pack(anchor="w", padx=20, pady=(20, 15))

        datos = [
            ("Nombre completo", "María López García"),
            ("Correo electrónico", "maria.lopez@immujer.gob.mx"),
            ("Teléfono", "953 123 4567"),
            ("Fecha de registro", "15/03/2024")
        ]

        for titulo, valor in datos:
            row_frame = ctk.CTkFrame(card_info, fg_color="transparent")
            row_frame.pack(fill="x", padx=20, pady=5)
            ctk.CTkLabel(row_frame, text=titulo, font=("Arial", 11, "bold"), text_color="gray").pack(anchor="w")
            ctk.CTkLabel(row_frame, text=valor, font=("Arial", 13), text_color="black").pack(anchor="w")
            ctk.CTkFrame(card_info, height=1, fg_color="#F0F0F0").pack(fill="x", padx=20, pady=5) 

        card_qr = ctk.CTkFrame(main_container, fg_color="white", corner_radius=15, border_width=1, border_color="#E0E0E0")
        card_qr.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        ctk.CTkLabel(card_qr, text="Escanea el código QR para acceder", font=("Arial", 16, "bold"), text_color="#006B4D").pack(anchor="w", padx=20, pady=(20, 5))

        qr_frame = ctk.CTkFrame(card_qr, width=200, height=200, fg_color="#F0F0F0", corner_radius=10, border_width=2, border_color="#FF6B35")
        qr_frame.pack(pady=10)
        qr_frame.pack_propagate(False)
        ctk.CTkLabel(qr_frame, text="Imagen QR ", text_color="gray").pack(expand=True)

        bottom_qr_frame = ctk.CTkFrame(card_qr, fg_color="transparent")
        bottom_qr_frame.pack(fill="x", padx=20, pady=(10, 20), side="bottom")
        
