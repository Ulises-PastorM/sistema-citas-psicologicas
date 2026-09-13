# -*- mode: python ; coding: utf-8 -*-

import os
import shutil

from PyInstaller.building.build_main import Analysis
from PyInstaller.building.api import PYZ, EXE, COLLECT


# ============================================================
# Directorio raíz del proyecto
# ============================================================

PROJECT_DIR = os.path.abspath(os.path.dirname(__name__))


# ============================================================
# Análisis
# ============================================================

a = Analysis(
    ['main.py'],
    pathex=[PROJECT_DIR],
    binaries=[],
    datas=[
        ('assets', 'assets'),
        ('database', 'database'),
        ('integrations', 'integrations'),
        ('runtime', 'runtime'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)


# ============================================================
# PYZ
# ============================================================

pyz = PYZ(a.pure)


# ============================================================
# Ejecutable
# ============================================================

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)


# ============================================================
# Colección
# ============================================================

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)


# ============================================================
# Mover carpetas externas fuera de _internal
# ============================================================

DIST_DIR = os.path.join(PROJECT_DIR, 'dist', 'main')
INTERNAL_DIR = os.path.join(DIST_DIR, '_internal')


CARPETAS_EXTERNAS = [
    'integrations',
    'runtime'
]


for carpeta in CARPETAS_EXTERNAS:

    origen = os.path.join(INTERNAL_DIR, carpeta)
    destino = os.path.join(DIST_DIR, carpeta)

    if os.path.exists(destino):
        shutil.rmtree(destino)

    if os.path.exists(origen):
        shutil.move(origen, destino)