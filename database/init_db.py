import pyodbc  # Importar el módulo pyodbc
from config.odbc_config import DatabaseConfig

def crear_tablas():
    """Crea las tablas necesarias en la base de datos"""
    db_config = DatabaseConfig()
    conn = None
    cursor = None

    try:
        conn = db_config.get_connection()
        if conn is None:
            raise Exception("No se pudo obtener la conexión a la base de datos.")
        
        cursor = conn.cursor()
        
        # Crear tabla de carreras
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS carreras (
            id INTEGER PRIMARY KEY IDENTITY(1,1),
            nombre VARCHAR(100) UNIQUE NOT NULL
        )
        """)
        print("✅ Tabla 'carreras' creada o ya existe.")

        # Crear tabla de estudiantes con relación a carreras
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS estudiantes (
            id INTEGER PRIMARY KEY IDENTITY(1,1),
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

    except (Exception, pyodbc.Error) as error:
        print(f"❌ Error al crear tablas: {error}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            db_config.release_connection(conn)

if __name__ == "__main__":
    crear_tablas()