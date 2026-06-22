const express = require('express');
const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode');
const qrcodeTerminal = require('qrcode-terminal');

// ─── Configuración ───────────────────────────────────────────────────────────
const PORT = process.env.PORT || 3000;
const app = express();
app.use(express.json());

// ─── Estado global de la sesión ───────────────────────────────────────────────
let sessionState = {
  status: 'disconnected',
  qrString: null,
  qrImage: null,
  clientInfo: null,
};

// ─── Inicializar cliente WhatsApp ─────────────────────────────────────────────
const client = new Client({
  authStrategy: new LocalAuth({
    dataPath: './sessions',
  }),
  puppeteer: {
    headless: true,
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-dev-shm-usage',
      '--disable-accelerated-2d-canvas',
      '--no-first-run',
      '--no-zygote',
      '--disable-gpu',
    ],
    // ✅ Darle más tiempo a WhatsApp Web para cargar antes de inyectar scripts
    timeout: 60000,
  },
  // ✅ Esperar más tiempo a que la página esté lista
  authTimeoutMs: 60000,
  qrMaxRetries: 5,
  restartOnAuthFail: true,
  // ✅ Ignorar errores de HTTPS en entornos corporativos / proxies
  webVersionCache: {
    type: 'remote',
    remotePath: 'https://raw.githubusercontent.com/wppconnect-team/wa-version/main/html/2.2412.54.html',
  },
});

// ─── Eventos del cliente ──────────────────────────────────────────────────────

client.on('qr', async (qr) => {
  console.log('\n📱 Nuevo código QR generado. Escanéalo en WhatsApp > Dispositivos vinculados.\n');
  qrcodeTerminal.generate(qr, { small: true });

  sessionState.status = 'qr_ready';
  sessionState.qrString = qr;
  sessionState.qrImage = await qrcode.toDataURL(qr);
});

client.on('ready', () => {
  const info = client.info;
  console.log(`\n✅ Sesión activa. Número conectado: ${info.wid.user}`);
  sessionState.status = 'connected';
  sessionState.qrString = null;
  sessionState.qrImage = null;
  sessionState.clientInfo = {
    number: info.wid.user,
    name: info.pushname,
    platform: info.platform,
  };
});

client.on('authenticated', () => {
  console.log('🔑 Sesión autenticada desde caché local.');
});

client.on('auth_failure', (msg) => {
  console.error('❌ Fallo de autenticación:', msg);
  sessionState.status = 'disconnected';
});

client.on('disconnected', (reason) => {
  console.warn('⚠️  Cliente desconectado:', reason);
  sessionState.status = 'disconnected';
  sessionState.clientInfo = null;
  console.log('🔄 Reconectando en 5 segundos...');
  setTimeout(() => iniciarCliente(), 5000);
});

// ─── Función de inicio con reintentos ─────────────────────────────────────────
let intentos = 0;
const MAX_INTENTOS = 5;

async function iniciarCliente() {
  try {
    intentos++;
    console.log(`⏳ Iniciando cliente WhatsApp... (intento ${intentos}/${MAX_INTENTOS})`);
    await client.initialize();
  } catch (err) {
    // ✅ Capturar el error "Execution context was destroyed" y reintentar
    if (err.message && err.message.includes('Execution context was destroyed')) {
      console.warn(`⚠️  WhatsApp Web recargó la página durante la inicialización.`);
    } else {
      console.error('❌ Error al inicializar el cliente:', err.message);
    }

    if (intentos < MAX_INTENTOS) {
      const espera = intentos * 3000; // espera progresiva: 3s, 6s, 9s...
      console.log(`🔄 Reintentando en ${espera / 1000} segundos...`);
      setTimeout(() => iniciarCliente(), espera);
    } else {
      console.error(`❌ Se alcanzó el máximo de reintentos (${MAX_INTENTOS}). Reinicia el servidor manualmente.`);
      intentos = 0;
    }
  }
}

// ─── Rutas REST ───────────────────────────────────────────────────────────────

app.get('/status', (req, res) => {
  res.json({
    status: sessionState.status,
    client: sessionState.clientInfo,
  });
});

app.get('/qr', (req, res) => {
  if (sessionState.status === 'connected') {
    return res.status(200).json({ message: 'Ya hay una sesión activa. No se necesita QR.' });
  }
  if (!sessionState.qrImage) {
    return res.status(503).json({ message: 'El QR aún no está listo. Intenta en unos segundos.' });
  }
  const base64Data = sessionState.qrImage.replace(/^data:image\/png;base64,/, '');
  const imgBuffer = Buffer.from(base64Data, 'base64');
  res.setHeader('Content-Type', 'image/png');
  res.send(imgBuffer);
});

app.post('/send-message', async (req, res) => {
  if (sessionState.status !== 'connected') {
    return res.status(503).json({ error: 'El cliente no está conectado. Escanea el QR primero.' });
  }

  const { phone, message } = req.body;

  if (!phone || !message) {
    return res.status(400).json({ error: 'Los campos "phone" y "message" son requeridos.' });
  }

  if (!/^\d{7,15}$/.test(phone)) {
    return res.status(400).json({
      error: 'Formato de número inválido. Usa solo dígitos con código de país. Ej: 521XXXXXXXXXX',
    });
  }

  try {
    const chatId = `${phone}@c.us`;
    const isRegistered = await client.isRegisteredUser(chatId);
    if (!isRegistered) {
      return res.status(404).json({ error: `El número ${phone} no está registrado en WhatsApp.` });
    }

    const response = await client.sendMessage(chatId, message);
    return res.json({
      success: true,
      messageId: response.id._serialized,
      to: phone,
      timestamp: response.timestamp,
    });
  } catch (err) {
    console.error('Error al enviar mensaje:', err);
    return res.status(500).json({ error: 'Error interno al enviar el mensaje.', detail: err.message });
  }
});

app.post('/send-media', async (req, res) => {
  if (sessionState.status !== 'connected') {
    return res.status(503).json({ error: 'El cliente no está conectado.' });
  }

  const { phone, url, caption } = req.body;

  if (!phone || !url) {
    return res.status(400).json({ error: 'Los campos "phone" y "url" son requeridos.' });
  }

  try {
    const { MessageMedia } = require('whatsapp-web.js');
    const media = await MessageMedia.fromUrl(url);
    const chatId = `${phone}@c.us`;
    const response = await client.sendMessage(chatId, media, { caption: caption || '' });
    return res.json({ success: true, messageId: response.id._serialized, to: phone });
  } catch (err) {
    console.error('Error al enviar media:', err);
    return res.status(500).json({ error: 'Error al enviar el archivo.', detail: err.message });
  }
});

// ─── Arrancar servidor HTTP ───────────────────────────────────────────────────
app.listen(PORT, () => {
  console.log(`\n🚀 Servidor REST escuchando en http://localhost:${PORT}`);
  console.log(`   GET  /status        → Estado de la sesión`);
  console.log(`   GET  /qr            → Código QR para escanear`);
  console.log(`   POST /send-message  → Enviar mensaje de texto`);
  console.log(`   POST /send-media    → Enviar imagen o archivo\n`);
});

// ─── Iniciar ──────────────────────────────────────────────────────────────────
iniciarCliente();
