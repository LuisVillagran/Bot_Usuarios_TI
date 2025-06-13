import sqlite3

conn = sqlite3.connect("soporte.db")
cursor = conn.cursor()

# Borrar tablas si existen
cursor.execute("DROP TABLE IF EXISTS tickets")
cursor.execute("DROP TABLE IF EXISTS usuarios")

# Crear tabla tickets
cursor.execute("""
CREATE TABLE tickets (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    estado TEXT NOT NULL,
    contrasena TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
)
""")

# Datos para usuarios
tickets = [
    (38591, "Ana Pérez", "Abierto", "clave123", "ana@gmail.com"),
    (90213, "Luis Soto", "Cerrado", "1234", "luis@gmail.com"),
    (18734, "Camila Rojas", "En proceso", "camila2024", "camila@gmail.com"),
    (62480, "Pedro Díaz", "Abierto", "p3dro!", "pedro@gmail.com"),
    (79304, "Valentina Campos", "En proceso", "valenpass", "valentina@gmail.com"),
    (58127, "Jorge Fuentes", "Cerrado", "jfuentes2023", "jorge@gmail.com"),
    (17098, "Sofía Vera", "Abierto", "sofia_2024", "sofia@gmail.com"),
    (45602, "Ricardo Núñez", "Abierto", "r123", "ricardo@gmail.com"),
    (83209, "María López", "Cerrado", "mlopez", "maria@gmail.com"),
    (71456, "Tomás Herrera", "En proceso", "th2025", "tomas@gmail.com")
]

# Insertar tickets
cursor.executemany("INSERT OR IGNORE INTO tickets (id, nombre, estado, contrasena, email) VALUES (?, ?, ?, ?, ?)", tickets)
conn.commit()
conn.close()

# Funcion encargada de ejecutar la query
def ejecutar_query(query):
    try:
        conn = sqlite3.connect("soporte.db")
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        conn.commit()
        conn.close()
        return str(result)
    except Exception as e:
        return f"Error ejecutando la query: {e}"
