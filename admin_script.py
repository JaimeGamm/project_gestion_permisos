import hashlib
import mysql.connector

# Conectar a la base de datos MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",  # Reemplaza con tu usuario de MySQL
    password="",  # Reemplaza con tu contraseña de MySQL
    database="gestion_permisos_2db"  # Reemplaza con tu base de datos correcta
)

cursor = conn.cursor()

# Datos del administrador
username = "admin"
password = "admin123"

# Encriptar la contraseña con MD5
hashed_password = hashlib.md5(password.encode()).hexdigest()

# Consulta de inserción en la tabla usuarios (no administradores)
query = "INSERT INTO usuarios (nombre, email, password, rol) VALUES (%s, %s, %s, %s)"
values = (username, "admin@example.com", hashed_password, "administrador")

try:
    cursor.execute(query, values)
    conn.commit()
    print("Usuario administrador agregado exitosamente.")
except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    cursor.close()
    conn.close()
