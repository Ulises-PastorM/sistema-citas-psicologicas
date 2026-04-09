from database.connection import get_connection, enable_foreign_keys

def crear_usuaria(nombre, fecha_ingreso, colonia, edad, telefono, problematica, estatus_id):
    conn = get_connection()
    enable_foreign_keys(conn)

    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO usuarias (nombre, fecha_ingreso, colonia, edad, telefono, problematica, estatus_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (nombre, fecha_ingreso, colonia, edad, telefono, problematica, estatus_id))

    conn.commit()
    conn.close()

def obtener_usuarias():
    conn = get_connection()
    enable_foreign_keys(conn)

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarias")

    resultados = cursor.fetchall()
    conn.close()

    return [dict(row) for row in resultados]