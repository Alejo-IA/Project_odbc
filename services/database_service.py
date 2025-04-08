import pyodbc
import random
from models.estudiante import Estudiante

class EstudianteService:
    def __init__(self, db_config):
        self.db_config = db_config

    def generar_id_aleatorio(self):
        """Genera un ID aleatorio de 5 dígitos que no esté en uso."""
        conexion = self.db_config.get_connection()
        if not conexion:
            print("❌ No se pudo obtener conexión a la base de datos.")
            return None
        try:
            cursor = conexion.cursor()
            while True:
                nuevo_id = random.randint(10000, 99999)  # Generar un número aleatorio de 5 dígitos
                cursor.execute("SELECT id FROM estudiantes WHERE id = ?", (nuevo_id,))
                if not cursor.fetchone():  # Si no existe en la base de datos, usar este ID
                    return nuevo_id
        except pyodbc.Error as error:
            print(f"⚠️ Error al generar ID aleatorio: {error}")
            return None
        finally:
            self.db_config.release_connection(conexion)

    def insertar(self, estudiante):
        """Crear nuevo estudiante"""
        conexion = self.db_config.get_connection()
        if not conexion:
            print("❌ No se pudo obtener conexión a la base de datos.")
            return None
        try:
            cursor = conexion.cursor()

            # Generar un ID aleatorio único
            estudiante.id = self.generar_id_aleatorio()
            if not estudiante.id:
                print("❌ No se pudo generar un ID único para el estudiante.")
                return None

            # Obtener ID de la carrera o crearla si no existe
            cursor.execute("SELECT id FROM carreras WHERE nombre = ?", (estudiante.carrera,))
            carrera_id = cursor.fetchone()
            
            if not carrera_id:
                print(f"⚠️ La carrera '{estudiante.carrera}' no existe. Creándola automáticamente...")
                cursor.execute("INSERT INTO carreras (nombre) VALUES (?)", (estudiante.carrera,))
                conexion.commit()
                cursor.execute("SELECT id FROM carreras WHERE nombre = ?", (estudiante.carrera,))
                carrera_id = cursor.fetchone()

            # Insertar estudiante
            query = """
            INSERT INTO estudiantes (id, nombre, edad, carrera_id, correo, fecha_ingreso) 
            VALUES (?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query, (estudiante.id, estudiante.nombre, estudiante.edad, carrera_id[0], estudiante.correo, estudiante.fecha_ingreso))
            conexion.commit()
            print(f"✅ Estudiante '{estudiante.nombre}' insertado con éxito con ID {estudiante.id}.")
            return True
        except pyodbc.Error as error:
            print(f"⚠️ Error al crear estudiante: {error}")
            conexion.rollback()
            return None
        finally:
            self.db_config.release_connection(conexion)

    def obtener_todos(self):
        """Obtener todos los estudiantes con el nombre de la carrera"""
        conexion = self.db_config.get_connection()
        if not conexion:
            print("❌ No se pudo obtener conexión a la base de datos.")
            return []
        try:
            cursor = conexion.cursor()
            query = """
            SELECT e.id, e.nombre, e.edad, c.nombre AS carrera, e.correo, e.fecha_ingreso
            FROM estudiantes e
            LEFT JOIN carreras c ON e.carrera_id = c.id
            ORDER BY e.id
            """
            cursor.execute(query)
            estudiantes = [Estudiante(*row) for row in cursor.fetchall()]
            print(f"✅ {len(estudiantes)} estudiantes obtenidos.")
            return estudiantes
        except pyodbc.Error as error:
            print(f"⚠️ Error al obtener estudiantes: {error}")
            return []
        finally:
            self.db_config.release_connection(conexion)

    def obtener_por_id(self, id_estudiante):
        """Obtener un estudiante por su ID"""
        conexion = self.db_config.get_connection()
        if not conexion:
            print("❌ No se pudo obtener conexión a la base de datos.")
            return None
        try:
            cursor = conexion.cursor()
            query = """
            SELECT e.id, e.nombre, e.edad, c.nombre AS carrera, e.correo, e.fecha_ingreso
            FROM estudiantes e
            LEFT JOIN carreras c ON e.carrera_id = c.id
            WHERE e.id = ?
            """
            cursor.execute(query, (id_estudiante,))
            row = cursor.fetchone()
            return Estudiante(*row) if row else None
        except pyodbc.Error as error:
            print(f"⚠️ Error al obtener estudiante por ID: {error}")
            return None
        finally:
            self.db_config.release_connection(conexion)

    def actualizar(self, estudiante):
        """Actualizar información de un estudiante"""
        conexion = self.db_config.get_connection()
        if not conexion:
            print("❌ No se pudo obtener conexión a la base de datos.")
            return False
        try:
            cursor = conexion.cursor()

            # Obtener ID de la carrera o crearla si no existe
            cursor.execute("SELECT id FROM carreras WHERE nombre = ?", (estudiante.carrera,))
            carrera_id = cursor.fetchone()
            
            if not carrera_id:
                print(f"⚠️ La carrera '{estudiante.carrera}' no existe. Creándola automáticamente...")
                cursor.execute("INSERT INTO carreras (nombre) VALUES (?)", (estudiante.carrera,))
                conexion.commit()
                cursor.execute("SELECT id FROM carreras WHERE nombre = ?", (estudiante.carrera,))
                carrera_id = cursor.fetchone()

            query = """
            UPDATE estudiantes 
            SET nombre=?, edad=?, carrera_id=?, correo=?, fecha_ingreso=?
            WHERE id=?
            """
            cursor.execute(query, (estudiante.nombre, estudiante.edad, carrera_id[0], estudiante.correo, estudiante.fecha_ingreso, estudiante.id))
            conexion.commit()
            return cursor.rowcount > 0  # True si se actualizó alguna fila
        except pyodbc.Error as error:
            print(f"⚠️ Error al actualizar estudiante: {error}")
            conexion.rollback()
            return False
        finally:
            self.db_config.release_connection(conexion)

    def eliminar(self, id_estudiante):
        """Eliminar un estudiante por su ID"""
        conexion = self.db_config.get_connection()
        if not conexion:
            print("❌ No se pudo obtener conexión a la base de datos.")
            return False
        try:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM estudiantes WHERE id = ?", (id_estudiante,))
            conexion.commit()
            return cursor.rowcount > 0  # True si se eliminó alguna fila
        except pyodbc.Error as error:
            print(f"⚠️ Error al eliminar estudiante: {error}")
            conexion.rollback()
            return False
        finally:
            self.db_config.release_connection(conexion)