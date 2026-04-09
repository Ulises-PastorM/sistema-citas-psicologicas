from connection import get_connection, enable_foreign_keys

def init_db():
    conn = get_connection()
    if conn is None:
        return

    enable_foreign_keys(conn)

    with open("database/schema.sql", "r", encoding="utf-8") as f:
        sql_script = f.read()

    conn.executescript(sql_script)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()