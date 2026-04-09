import sqlite3
from sqlite3 import Error
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "immujer.db")


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
    conn.execute("PRAGMA foreign_keys = ON;")