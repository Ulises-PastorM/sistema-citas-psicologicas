require('./patch-local-auth');

const express = require('express');
const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode');
const qrcodeTerminal = require('qrcode-terminal');
const { execSync } = require('child_process');

const PORT = process.env.PORT || 3000;
const app  = express();
app.use(express.json());

let sessionState = {
  status: 'disconnected',
  qrString: null,
  qrImage: null,
  clientInfo: null,
};

let client    = null;
let intentos  = 0;
let chromePID = null;
const MAX_INTENTOS = 5;

const CLIENT_OPTS = {
  authStrategy: new LocalAuth({ dataPath: './sessions' }),
  puppeteer: {
    headless: true,
    args: [
      '--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage',
      '--disable-accelerated-2d-canvas', '--no-first-run', '--no-zygote', '--disable-gpu',
    ],
    timeout: 60000,
  },
  authTimeoutMs: 60000,
  qrMaxRetries: 5,
  restartOnAuthFail: true,
  webVersionCache: {
    type: 'remote',
    remotePath: 'https://raw.githubusercontent.com/wppconnect-team/wa-version/main/html/2.2412.54.html',
  },
};

// ─── Matar Chrome por PID ─────────────────────────────────────────────────────
function matarChrome(pid) {
  if (!pid) return;
  try {
    if (process.platform === 'win32') {
      execSync(`taskkill /F /T /PID ${pid}`, { stdio: 'ignore' });
    } else {
      execSync(`kill -9 ${pid}`, { stdio: 'ignore' });
    }
    console.log(`🧹 Chrome (PID ${pid}) terminado.`);
  } catch (_) {
    console.log(`🧹 Chrome (PID ${pid}) ya no estaba corriendo.`);
  }
  chromePID = null;
}

// ─── Fábrica de cliente ───────────────────────────────────────────────────────
function crearCliente() {
  const c = new Client(CLIENT_OPTS);

  c.on('qr', async (qr) => {
    if (!chromePID && c.pupBrowser) {
      chromePID = c.pupBrowser.process()?.pid || null;
      if (chromePID) console.log(`🌐 Chrome iniciado (PID: ${chromePID})`);
    }
    console.log('\n📱 Nuevo QR generado. Escanéalo en WhatsApp > Dispositivos vinculados.\n');
    qrcodeTerminal.generate(qr, { small: true });
    sessionState.status   = 'qr_ready';
    sessionState.qrString = qr;
    sessionState.qrImage  = await qrcode.toDataURL(qr);
  });

  c.on('ready', () => {
    if (!chromePID && c.pupBrowser) {
      chromePID = c.pupBrowser.process()?.pid || null;
      if (chromePID) console.log(`🌐 Chrome activo (PID: ${chromePID})`);
    }
    const info = c.info;
    console.log(`\n✅ Sesión activa. Número conectado: ${info.wid.user}`);
    intentos = 0;
    sessionState.status     = 'connected';
    sessionState.qrString   = null;
    sessionState.qrImage    = null;
    sessionState.clientInfo = { number: info.wid.user, name: info.pushname, platform: info.platform };
  });

  c.on('authenticated', () => console.log('🔑 Sesión autenticada desde caché local.'));

  c.on('auth_failure', (msg) => {
    console.error('❌ Fallo de autenticación:', msg);
    sessionState.status = 'disconnected';
  });

  c.on('disconnected', async (reason) => {
    console.warn(`⚠️  Cliente desconectado: ${reason}`);
    sessionState.status     = 'disconnected';
    sessionState.clientInfo = null;
    sessionState.qrString   = null;
    sessionState.qrImage    = null;

    if (reason === 'LOGOUT') {
      console.log('🔄 Preparando nuevo cliente en 3 segundos...');
      setTimeout(() => { intentos = 0; client = crearCliente(); iniciarCliente(); }, 3000);
    } else {
      console.log('🔄 Reconectando en 5 segundos...');
      setTimeout(() => iniciarCliente(), 5000);
    }
  });

  return c;
}

// ─── Inicialización con reintentos ────────────────────────────────────────────
async function iniciarCliente() {
  try {
    intentos++;
    console.log(`⏳ Iniciando cliente WhatsApp... (intento ${intentos}/${MAX_INTENTOS})`);
    await client.initialize();
  } catch (err) {

    // Caso 1: Chrome quedó huérfano de un intento anterior → matarlo y reintentar
    if (err.message?.includes('browser is already running')) {
      console.warn('⚠️  Chrome huérfano detectado. Terminándolo...');
      matarChrome(chromePID);
      // Intentar obtener el PID desde el mensaje de error si no lo tenemos
      if (!chromePID) {
        // Dar tiempo a que el proceso se limpie antes de reintentar
        await new Promise(r => setTimeout(r, 3000));
      }
      // Crear cliente nuevo (el viejo tiene el browser en estado inválido)
      client = crearCliente();
      if (intentos < MAX_INTENTOS) {
        const espera = intentos * 3000;
        console.log(`🔄 Reintentando en ${espera / 1000} segundos...`);
        setTimeout(() => iniciarCliente(), espera);
      }
      return;
    }

    // Caso 2: WhatsApp Web navegó durante la inyección → solo reintentar
    if (err.message?.includes('Execution context was destroyed')) {
      console.warn('⚠️  WhatsApp Web recargó la página. Matando Chrome y reintentando...');
      matarChrome(chromePID);
      client = crearCliente();
      if (intentos < MAX_INTENTOS) {
        const espera = intentos * 3000;
        console.log(`🔄 Reintentando en ${espera / 1000} segundos...`);
        setTimeout(() => iniciarCliente(), espera);
      }
      return;
    }

    // Caso 3: Error desconocido
    console.error('❌ Error al inicializar el cliente:', err.message);
    if (intentos < MAX_INTENTOS) {
      const espera = intentos * 3000;
      console.log(`🔄 Reintentando en ${espera / 1000} segundos...`);
      setTimeout(() => iniciarCliente(), espera);
    } else {
      console.error(`❌ Máximo de reintentos alcanzado. Reinicia el servidor manualmente.`);
      intentos = 0;
    }
  }
}

// ─── Rutas REST ───────────────────────────────────────────────────────────────

app.get('/status', (req, res) => {
  res.json({ status: sessionState.status, client: sessionState.clientInfo });
});

app.get('/qr', (req, res) => {
  if (sessionState.status === 'connected')
    return res.status(200).json({ message: 'Ya hay una sesión activa. No se necesita QR.' });
  if (!sessionState.qrImage)
    return res.status(503).json({ message: 'El QR aún no está listo. Intenta en unos segundos.' });
  const imgBuffer = Buffer.from(sessionState.qrImage.replace(/^data:image\/png;base64,/, ''), 'base64');
  res.setHeader('Content-Type', 'image/png');
  res.send(imgBuffer);
});

app.post('/send-message', async (req, res) => {
  if (sessionState.status !== 'connected')
    return res.status(503).json({ error: 'El cliente no está conectado. Escanea el QR primero.' });
  const { phone, message } = req.body;
  if (!phone || !message)
    return res.status(400).json({ error: 'Los campos "phone" y "message" son requeridos.' });
  if (!/^\d{7,15}$/.test(phone))
    return res.status(400).json({ error: 'Formato de número inválido. Ej: 521XXXXXXXXXX' });
  try {
    const chatId = `${phone}@c.us`;
    if (!await client.isRegisteredUser(chatId))
      return res.status(404).json({ error: `El número ${phone} no está registrado en WhatsApp.` });
    const response = await client.sendMessage(chatId, message);
    return res.json({ success: true, messageId: response.id._serialized, to: phone, timestamp: response.timestamp });
  } catch (err) {
    console.error('Error al enviar mensaje:', err);
    return res.status(500).json({ error: 'Error interno.', detail: err.message });
  }
});

app.post('/send-media', async (req, res) => {
  if (sessionState.status !== 'connected')
    return res.status(503).json({ error: 'El cliente no está conectado.' });
  const { phone, url, caption } = req.body;
  if (!phone || !url)
    return res.status(400).json({ error: 'Los campos "phone" y "url" son requeridos.' });
  try {
    const { MessageMedia } = require('whatsapp-web.js');
    const response = await client.sendMessage(`${phone}@c.us`, await MessageMedia.fromUrl(url), { caption: caption || '' });
    return res.json({ success: true, messageId: response.id._serialized, to: phone });
  } catch (err) {
    console.error('Error al enviar media:', err);
    return res.status(500).json({ error: 'Error al enviar el archivo.', detail: err.message });
  }
});

// ─── Arrancar ─────────────────────────────────────────────────────────────────
app.listen(PORT, () => {
  console.log(`\n🚀 Servidor REST escuchando en http://localhost:${PORT}`);
  console.log(`   GET  /status        → Estado de la sesión`);
  console.log(`   GET  /qr            → Código QR para escanear`);
  console.log(`   POST /send-message  → Enviar mensaje de texto`);
  console.log(`   POST /send-media    → Enviar imagen o archivo\n`);
});

client = crearCliente();
iniciarCliente();