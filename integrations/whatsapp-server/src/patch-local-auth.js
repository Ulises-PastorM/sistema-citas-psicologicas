/**
 * patch-local-auth.js
 * 
 * Parchea LocalAuth de whatsapp-web.js para que en Windows no lance
 * un error fatal cuando los archivos .db-journal están bloqueados (EBUSY).
 * En lugar de lanzar, espera y reintenta el borrado.
 * 
 * Uso: require('./patch-local-auth') antes de crear el Client.
 */

const fs   = require('fs');
const path = require('path');

const LOCAL_AUTH_PATH = require.resolve(
  'whatsapp-web.js/src/authStrategies/LocalAuth'
);

const LocalAuth = require(LOCAL_AUTH_PATH);

// Guardar el logout original
const _logoutOriginal = LocalAuth.prototype.logout;

LocalAuth.prototype.logout = async function () {
  const sessionDir = this.userDataDir;   // ruta completa a sessions/session

  if (!sessionDir || !fs.existsSync(sessionDir)) {
    return;   // nada que borrar
  }

  const MAX_INTENTOS = 10;
  const ESPERA_MS    = 1500;

  for (let i = 0; i < MAX_INTENTOS; i++) {
    try {
      fs.rmSync(sessionDir, { recursive: true, force: true });
      console.log('🗑️  Carpeta de sesión eliminada correctamente.');
      return;
    } catch (err) {
      if (err.code === 'EBUSY' || err.code === 'ENOTEMPTY' || err.code === 'EPERM') {
        console.log(`⏳ Archivos aún bloqueados, reintentando... (${i + 1}/${MAX_INTENTOS})`);
        await new Promise(r => setTimeout(r, ESPERA_MS));
      } else {
        // Error distinto a bloqueo — lanzar normalmente
        throw err;
      }
    }
  }

  console.warn('⚠️  No se pudo eliminar la carpeta de sesión después de varios intentos. Continuando...');
};

console.log('🔧 LocalAuth parcheado para manejo de EBUSY en Windows.');