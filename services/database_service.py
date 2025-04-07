import psycopg2
from models.estudiante import Estudiante

class EstudianteService:
    def __init__(self, db_config):
        self.db_config = db_config

    def insertar(self, estudiante):
        """Crear nuevo estudiante"""
        conexion = self.db_config.get_connection()
        if not conexion:
            print("❌ No se pudo obtener conexión a la base de datos.")
            return None
        try:
            with conexion.cursor() as cursor:
                # Obtener ID de la carrera o crearla si no existe
                cursor.execute("SELECT id FROM carreras WHERE nombre = %s", (estudiante.carrera,))
                carrera_id = cursor.fetchone()
                
                if not carrera_id:
                    print(f"⚠️ La carrera '{estudiante.carrera}' no existe. Creándola automáticamente...")
                    cursor.execute("INSERT INTO carreras (nombre) VALUES (%s) RETURNING id", (estudiante.carrera,))
                    carrera_id = cursor.fetchone()
                
                query = """
                INSERT INTO estudiantes (nombre, edad, carrera_id, correo, fecha_ingreso) 
                VALUES (%s, %s, %s, %s, %s) RETURNING id
                """
                cursor.execute(query, (estudiante.nombre, estudiante.edad, carrera_id[0], estudiante.correo, estudiante.fecha_ingreso))
                estudiante_id = cursor.fetchone()
                conexion.commit()
                return estudiante_id[0] if estudiante_id else None
        except (Exception, psycopg2.Error) as error:
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
            with conexion.cursor() as cursor:
                query = """
                SELECT e.id, e.nombre, e.edad, c.nombre AS carrera, e.correo, e.fecha_ingreso
                FROM estudiantes e
                LEFT JOIN carreras c ON e.carrera_id = c.id
                ORDER BY e.id
                """
                cursor.execute(query)
                return [Estudiante(*row) for row in cursor.fetchall()]
        except (Exception, psycopg2.Error) as error:
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
            with conexion.cursor() as cursor:
                query = """
                SELECT e.id, e.nombre, e.edad, c.nombre AS carrera, e.correo, e.fecha_ingreso
                FROM estudiantes e
                LEFT JOIN carreras c ON e.carrera_id = c.id
                WHERE e.id = %s
                """
                cursor.execute(query, (id_estudiante,))
                row = cursor.fetchone()
                return Estudiante(*row) if row else None
        except (Exception, psycopg2.Error) as error:
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
            with conexion.cursor() as cursor:
                # Obtener ID de la carrera o crearla si no existe
                cursor.execute("SELECT id FROM carreras WHERE nombre = %s", (estudiante.carrera,))
                carrera_id = cursor.fetchone()
                
                if not carrera_id:
                    print(f"⚠️ La carrera '{estudiante.carrera}' no existe. Creándola automáticamente...")
                    cursor.execute("INSERT INTO carreras (nombre) VALUES (%s) RETURNING id", (estudiante.carrera,))
                    carrera_id = cursor.fetchone()
                
                query = """
                UPDATE estudiantes 
                SET nombre=%s, edad=%s, carrera_id=%s, correo=%s, fecha_ingreso=%s
                WHERE id=%s
                """
                cursor.execute(query, (estudiante.nombre, estudiante.edad, carrera_id[0], estudiante.correo, estudiante.fecha_ingreso, estudiante.id))
                conexion.commit()
                return cursor.rowcount > 0  # True si se actualizó alguna fila
        except (Exception, psycopg2.Error) as error:
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
            with conexion.cursor() as cursor:
                cursor.execute("DELETE FROM estudiantes WHERE id = %s", (id_estudiante,))
                conexion.commit()
                return cursor.rowcount > 0  # True si se eliminó alguna fila
        except (Exception, psycopg2.Error) as error:
            print(f"⚠️ Error al eliminar estudiante: {error}")
            conexion.rollback()
            return False
        finally:
            self.db_config.release_connection(conexion)