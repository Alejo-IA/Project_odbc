import os
import pyodbc
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

class DatabaseConfig:
    def __init__(self):
        """Inicializa la configuración de la base de datos mediante ODBC."""
        self.dsn = os.getenv('DB_DSN', 'Postgres_ODBC')  # Nombre del DSN configurado
        self.user = os.getenv('DB_USER', 'postgres')
        self.password = os.getenv('DB_PASSWORD', 'tu_contraseña')

    def get_connection(self):
        """Obtiene una conexión ODBC."""
        try:
            connection = pyodbc.connect(
                f"DSN={self.dsn};UID={self.user};PWD={self.password}",
                autocommit=True
            )
            print("✅ Conexión ODBC establecida exitosamente.")
            return connection
        except pyodbc.Error as error:
            print(f"❌ Error al conectar con la base de datos mediante ODBC: {error}")
            return None

    def release_connection(self, connection):
        """Cierra la conexión ODBC."""
        if connection:
            connection.close()
            print("🔒 Conexión ODBC cerrada correctamente.")


def crear_base_de_datos_y_tabla():
    """Crear la base de datos y las tablas necesarias si no existen."""
    db_config = DatabaseConfig()

    try:
        # Conectar a la base de datos mediante ODBC
        conn = db_config.get_connection()
        if not conn:
            raise Exception("No se pudo establecer la conexión a la base de datos mediante ODBC.")

        cursor = conn.cursor()

        # Crear tabla de carreras
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS carreras (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(100) UNIQUE NOT NULL
        )
        """)
        print("✅ Tabla 'carreras' creada o ya existe.")

        # Crear tabla de estudiantes con relación a carreras
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS estudiantes (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            edad INTEGER NOT NULL,
            carrera_id INTEGER NOT NULL REFERENCES carreras(id),
            correo VARCHAR(100) UNIQUE,
            fecha_ingreso DATE DEFAULT CURRENT_DATE
        )
        """)
        print("✅ Tabla 'estudiantes' creada o ya existe.")

        conn.commit()
        print("✅ Tablas creadas exitosamente.")

    except pyodbc.Error as error:
        print(f"❌ Error al crear tablas: {error}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            db_config.release_connection(conn)


# Ejecutar creación de base de datos y tablas
if __name__ == "__main__":
    crear_base_de_datos_y_tabla()