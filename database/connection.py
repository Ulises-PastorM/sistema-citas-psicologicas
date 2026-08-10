from pathlib import Path
import sys
import sqlite3
from sqlite3 import Error

if getattr(sys, "frozen", False):
    # main.exe
    BASE_DIR = Path(sys.executable).parent / "_internal"
else:
    # Proyecto en desarrollo
    BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "database" / "immujer.db"


def get_connection():
    try:
        conn = sqlite3.connect(DB_PATH)
        #Habilita el acceso por nombre de columna
        conn.row_factory = sqlite3.Row
        return conn
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

#Habilita el uso de llaves foráneas
def enable_foreign_keys(conn):
    if conn is not None:
        conn.execute("PRAGMA foreign_keys = ON;")