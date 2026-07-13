import threading
import io
import requests
from PIL import Image
import customtkinter as ctk
from services.whatsapp_services import obtener_estado_servidor

WHATSAPP_SERVER_URL = "http://localhost:3000"


class MiCuentaView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._qr_polling = False   # controla el loop de refresco del QR

        # ─── Header ──────────────────────────────────────────────────────────
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))

        titulos_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        titulos_frame.pack(side="left")
        ctk.CTkLabel(
            titulos_frame, text="Mi Cuenta",
            font=("Arial", 22, "bold"), text_color="#006B4D"
        ).pack(anchor="w")

        # ─── Contenedor principal ─────────────────────────────────────────────
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.grid(row=1, column=0, sticky="nsew")
        main_container.grid_columnconfigure(0, weight=1, uniform="col")
        main_container.grid_columnconfigure(1, weight=1, uniform="col")
        main_container.grid_rowconfigure(0, weight=1)

        # ─── Card: Información Personal ───────────────────────────────────────
        card_info = ctk.CTkFrame(
            main_container, fg_color="white",
            corner_radius=15, border_width=1, border_color="#E0E0E0"
        )
        card_info.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        ctk.CTkLabel(
            card_info, text="Información Personal",
            font=("Arial", 16, "bold"), text_color="#006B4D"
        ).pack(anchor="w", padx=20, pady=(20, 15))

        datos = [
            ("Nombre completo",    "María López García"),
            ("Correo electrónico", "maria.lopez@immujer.gob.mx"),
            ("Teléfono",           "953 123 4567"),
            ("Fecha de registro",  "15/03/2024"),
        ]

        for titulo, valor in datos:
            row_frame = ctk.CTkFrame(card_info, fg_color="transparent")
            row_frame.pack(fill="x", padx=20, pady=5)
            ctk.CTkLabel(row_frame, text=titulo, font=("Arial", 11, "bold"), text_color="gray").pack(anchor="w")
            ctk.CTkLabel(row_frame, text=valor,  font=("Arial", 13),         text_color="black").pack(anchor="w")
            ctk.CTkFrame(card_info, height=1, fg_color="#F0F0F0").pack(fill="x", padx=20, pady=5)

        # ─── Card: QR WhatsApp ────────────────────────────────────────────────
        card_qr = ctk.CTkFrame(
            main_container, fg_color="white",
            corner_radius=15, border_width=1, border_color="#E0E0E0"
        )
        card_qr.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        ctk.CTkLabel(
            card_qr, text="Conexión WhatsApp",
            font=("Arial", 16, "bold"), text_color="#006B4D"
        ).pack(anchor="w", padx=20, pady=(20, 5))

        # Label de estado (🟢 / 🔴 / 🟡)
        self.lbl_estado_wa = ctk.CTkLabel(
            card_qr, text="🔄 Verificando...",
            font=("Arial", 12), text_color="#888888"
        )
        self.lbl_estado_wa.pack(anchor="w", padx=20, pady=(0, 10))

        # Contenedor del QR
        self.qr_frame = ctk.CTkFrame(
            card_qr, width=220, height=220,
            fg_color="#F0F0F0", corner_radius=10,
            border_width=2, border_color="#FF6B35"
        )
        self.qr_frame.pack(pady=10)
        self.qr_frame.pack_propagate(False)

        # Label dentro del frame: muestra imagen o texto placeholder
        self.lbl_qr = ctk.CTkLabel(self.qr_frame, text="", text_color="gray")
        self.lbl_qr.pack(expand=True)

        # Botón de refresco manual
        self.btn_refrescar = ctk.CTkButton(
            card_qr, text="🔄 Refrescar QR",
            fg_color="#FF6B35", hover_color="#cc5520",
            text_color="white", font=("Arial", 13, "bold"),
            corner_radius=8, height=38,
            command=self._refrescar_manual
        )
        self.btn_refrescar.pack(pady=(5, 20))

        # ─── Iniciar verificación al cargar la vista ──────────────────────────
        threading.Thread(target=self._ciclo_qr, daemon=True).start()

    # ─── Lógica del QR ────────────────────────────────────────────────────────

    def _ciclo_qr(self):
        """
        Loop que verifica el estado de WhatsApp cada 20s.
        - Si está conectado: muestra ícono de éxito y detiene el polling.
        - Si hay QR disponible: descarga y muestra la imagen.
        - Si el servidor no responde: muestra error.
        """
        self._qr_polling = True

        while self._qr_polling:
            estado = obtener_estado_servidor()
            status = estado.get("status")

            if status == "connected":
                info = estado.get("client", {})
                numero = info.get("number", "") if info else ""
                self.after(0, lambda n=numero: self._mostrar_conectado(n))
                self._qr_polling = False
                break

            elif status == "qr_ready":
                self.after(0, lambda: self.lbl_estado_wa.configure(
                    text="📱 Escanea el QR para vincular WhatsApp",
                    text_color="#E09000"
                ))
                self._descargar_y_mostrar_qr()

            elif status == "error":
                self.after(0, lambda: self._mostrar_error("Servidor no disponible"))
                self._qr_polling = False
                break

            else:
                # disconnected o qr aún no listo
                self.after(0, lambda: self.lbl_estado_wa.configure(
                    text="⏳ Esperando al servidor...",
                    text_color="#888888"
                ))
                self.after(0, lambda: self.lbl_qr.configure(text="Cargando...", image=None))

            # Esperar ~20s antes del siguiente check (tiempo de vida de un QR)
            import time
            time.sleep(10)

    def _descargar_y_mostrar_qr(self):
        """Descarga la imagen PNG del QR y la muestra en el label."""
        try:
            response = requests.get(f"{WHATSAPP_SERVER_URL}/qr", timeout=10)

            if response.status_code == 200 and response.headers.get("Content-Type") == "image/png":
                img_bytes = response.content
                img = Image.open(io.BytesIO(img_bytes)).resize((200, 200))
                ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(200, 200))

                # Actualizar UI desde el hilo principal
                self.after(0, lambda i=ctk_img: self._actualizar_imagen_qr(i))

            elif response.status_code == 200:
                # Responde JSON: sesión ya activa
                data = response.json()
                self.after(0, lambda: self._mostrar_conectado(""))

        except Exception as e:
            self.after(0, lambda: self._mostrar_error(f"Error al obtener QR: {e}"))

    def _actualizar_imagen_qr(self, ctk_img):
        self.lbl_qr.configure(image=ctk_img, text="")
        self.lbl_qr.image = ctk_img   # evitar garbage collection

    def _mostrar_conectado(self, numero: str):
        texto = f"🟢 WhatsApp conectado\n+{numero}" if numero else "🟢 WhatsApp conectado"
        self.lbl_estado_wa.configure(text=texto, text_color="#006B4D")

        # ✅ Limpiar imagen antes de poner el texto
        self.lbl_qr.configure(
            image=None,          # elimina la imagen del QR
            text="✅\nSesión activa",
            font=("Arial", 16, "bold"),
            text_color="#006B4D"
        )
        self.lbl_qr.image = None   # liberar referencia
        self.btn_refrescar.configure(state="disabled")

    def _mostrar_error(self, detalle: str):
        self.lbl_estado_wa.configure(text=f"🔴 {detalle}", text_color="#CC4400")
        self.lbl_qr.configure(text="Sin conexión\nal servidor", image=None, text_color="#CC4400")

    def _refrescar_manual(self):
        """Permite al usuario forzar una nueva verificación."""
        self._qr_polling = False   # detener el loop anterior
        self.lbl_estado_wa.configure(text="🔄 Verificando...", text_color="#888888")
        self.lbl_qr.configure(text="Cargando...", image=None, text_color="gray")
        self.btn_refrescar.configure(state="disabled")

        def _reanudar():
            import time
            time.sleep(0.5)
            self.after(0, lambda: self.btn_refrescar.configure(state="normal"))
            self._ciclo_qr()

        threading.Thread(target=_reanudar, daemon=True).start()