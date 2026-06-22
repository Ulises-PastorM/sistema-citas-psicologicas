# WhatsApp REST Server

Servidor local con Node.js que genera un código QR para autenticarse en WhatsApp
y expone una REST API para enviar mensajes.

---

## Requisitos previos

| Herramienta | Versión mínima | Cómo verificar         |
|-------------|---------------|------------------------|
| Node.js     | 18 o superior | `node --version`       |
| npm         | 9 o superior  | `npm --version`        |
| Google Chrome o Chromium | cualquiera | (Puppeteer lo usa internamente) |

> En Linux (Ubuntu/Debian) instala Chromium con:
> `sudo apt install -y chromium-browser`

---

## Instalación paso a paso

### 1. Clonar o crear la carpeta del proyecto

```bash
mkdir whatsapp-server
cd whatsapp-server
```

### 2. Instalar dependencias

```bash
npm install
```

Esto instalará:
- **whatsapp-web.js** — cliente de WhatsApp Web controlado por Puppeteer
- **express** — servidor HTTP para la REST API
- **qrcode** — genera el QR como imagen PNG
- **qrcode-terminal** — muestra el QR en consola
- **nodemon** (dev) — reinicia el servidor automáticamente al guardar cambios

### 3. Estructura de carpetas resultante

```
whatsapp-server/
├── src/
│   └── index.js          ← Código principal del servidor
├── sessions/             ← Se crea automáticamente al escanear el QR
│   └── ...               ← Datos de sesión (no commitear)
├── package.json
├── .gitignore
└── README.md
```

---

## Uso

### Iniciar el servidor

```bash
# Modo producción
npm start

# Modo desarrollo (reinicia al guardar cambios)
npm run dev
```

### Primer inicio — Escanear el QR

1. Al correr el servidor verás un QR en la terminal.
2. En tu teléfono abre WhatsApp → **Dispositivos vinculados** → **Vincular un dispositivo**.
3. Escanea el QR.
4. La consola mostrará: `✅ Sesión activa. Número conectado: 521XXXXXXXXXX`

A partir del segundo inicio, la sesión se carga desde `./sessions/` automáticamente
y no necesitas volver a escanear.

---

## Endpoints REST

### `GET /status`
Devuelve el estado actual de la sesión.

```bash
curl http://localhost:3000/status
```

```json
{
  "status": "connected",
  "client": {
    "number": "521XXXXXXXXXX",
    "name": "Tu Nombre",
    "platform": "android"
  }
}
```

Los valores posibles de `status` son:
- `disconnected` — no hay sesión activa
- `qr_ready` — QR generado, esperando escaneo
- `connected` — sesión activa y lista para enviar mensajes

---

### `GET /qr`
Devuelve el QR como imagen PNG para incrustar en un navegador.

```bash
# Ver el QR en el navegador
open http://localhost:3000/qr

# O guardarlo como archivo
curl http://localhost:3000/qr -o qr.png
```

Si ya hay sesión activa responde:
```json
{ "message": "Ya hay una sesión activa. No se necesita QR." }
```

---

### `POST /send-message`
Envía un mensaje de texto.

```bash
curl -X POST http://localhost:3000/send-message \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "521XXXXXXXXXX",
    "message": "Hola desde el servidor 👋"
  }'
```

**Parámetros:**

| Campo     | Tipo   | Requerido | Descripción                                                    |
|-----------|--------|-----------|----------------------------------------------------------------|
| `phone`   | string | ✅        | Número con código de país, sin `+` ni espacios. Ej: `521XXXXXXXXXX` |
| `message` | string | ✅        | Texto del mensaje                                              |

**Respuesta exitosa:**
```json
{
  "success": true,
  "messageId": "true_521XXXXXXXXXX@c.us_XXXXXXXXXX",
  "to": "521XXXXXXXXXX",
  "timestamp": 1700000000
}
```

---

### `POST /send-media`
Envía una imagen o archivo desde una URL pública.

```bash
curl -X POST http://localhost:3000/send-media \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "521XXXXXXXXXX",
    "url": "https://example.com/imagen.jpg",
    "caption": "Mira esta imagen"
  }'
```

**Parámetros:**

| Campo     | Tipo   | Requerido | Descripción             |
|-----------|--------|-----------|-------------------------|
| `phone`   | string | ✅        | Número con código de país |
| `url`     | string | ✅        | URL pública del archivo |
| `caption` | string | ❌        | Texto opcional debajo del archivo |

---

## Códigos de error

| Código | Descripción                                              |
|--------|----------------------------------------------------------|
| 400    | Campos faltantes o formato de número inválido            |
| 404    | El número no está registrado en WhatsApp                 |
| 503    | El cliente no está conectado (escanea el QR primero)     |
| 500    | Error interno del servidor                               |

---

## Notas importantes

- El número en `phone` debe incluir el **código de país completo** sin `+`:
  - México: `521` + 10 dígitos → `521XXXXXXXXXX`
  - USA: `1` + 10 dígitos → `1XXXXXXXXXX`
- La carpeta `sessions/` contiene tu sesión de WhatsApp. **No la subas a Git.**
- Este servidor usa Puppeteer para controlar un Chrome headless. En servidores
  sin interfaz gráfica (Linux) puede requerirse instalar dependencias adicionales:
  ```bash
  sudo apt install -y ca-certificates fonts-liberation libasound2 \
    libatk-bridge2.0-0 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 \
    libexpat1 libfontconfig1 libgbm1 libgcc1 libglib2.0-0 libgtk-3-0 \
    libnspr4 libnss3 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 \
    libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 \
    libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 \
    lsb-release wget xdg-utils
  ```
