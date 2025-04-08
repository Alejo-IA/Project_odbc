from config.odbc_config import DatabaseConfig
from services.database_service import EstudianteService
from models.estudiante import Estudiante

def insertar_estudiantes_masivamente():
    db_config = DatabaseConfig()
    servicio = EstudianteService(db_config)

    # Lista de estudiantes a insertar
    estudiantes = [
        Estudiante(None, "Juan Pérez", 20, "Ingeniería", "juan.perez@example.com", "2025-04-01"),
        Estudiante(None, "María López", 22, "Medicina", "maria.lopez@example.com", "2025-04-02"),
        Estudiante(None, "Carlos García", 19, "Derecho", "carlos.garcia@example.com", "2025-04-03"),
        Estudiante(None, "Ana Torres", 21, "Arquitectura", "ana.torres@example.com", "2025-04-04"),
        Estudiante(None, "Luis Gómez", 23, "Economía", "luis.gomez@example.com", "2025-04-05"),
        Estudiante(None, "Sofía Martínez", 20, "Psicología", "sofia.martinez@example.com", "2025-04-06"),
        Estudiante(None, "Pedro Ramírez", 24, "Ingeniería", "pedro.ramirez@example.com", "2025-04-07"),
        Estudiante(None, "Laura Fernández", 22, "Medicina", "laura.fernandez@example.com", "2025-04-08"),
        Estudiante(None, "Diego Herrera", 21, "Derecho", "diego.herrera@example.com", "2025-04-09"),
        Estudiante(None, "Carolina Vega", 23, "Arquitectura", "carolina.vega@example.com", "2025-04-10"),
        Estudiante(None, "Jorge Ruiz", 20, "Economía", "jorge.ruiz@example.com", "2025-04-11"),
        Estudiante(None, "Valeria Castro", 19, "Psicología", "valeria.castro@example.com", "2025-04-12"),
        Estudiante(None, "Andrés Morales", 22, "Ingeniería", "andres.morales@example.com", "2025-04-13"),
        Estudiante(None, "Gabriela Ortiz", 21, "Medicina", "gabriela.ortiz@example.com", "2025-04-14"),
        Estudiante(None, "Ricardo Soto", 23, "Derecho", "ricardo.soto@example.com", "2025-04-15"),
        Estudiante(None, "Isabel Peña", 20, "Arquitectura", "isabel.pena@example.com", "2025-04-16"),
        Estudiante(None, "Fernando Díaz", 24, "Economía", "fernando.diaz@example.com", "2025-04-17"),
        Estudiante(None, "Camila Rojas", 19, "Psicología", "camila.rojas@example.com", "2025-04-18"),
        Estudiante(None, "Héctor Vargas", 21, "Ingeniería", "hector.vargas@example.com", "2025-04-19"),
        Estudiante(None, "Patricia Navarro", 22, "Medicina", "patricia.navarro@example.com", "2025-04-20"),
        Estudiante(None, "Manuel Castillo", 23, "Derecho", "manuel.castillo@example.com", "2025-04-21"),
        Estudiante(None, "Lucía Mendoza", 20, "Arquitectura", "lucia.mendoza@example.com", "2025-04-22"),
        Estudiante(None, "Álvaro Reyes", 24, "Economía", "alvaro.reyes@example.com", "2025-04-23"),
        Estudiante(None, "Daniela Paredes", 19, "Psicología", "daniela.paredes@example.com", "2025-04-24"),
        Estudiante(None, "Sebastián Cruz", 21, "Ingeniería", "sebastian.cruz@example.com", "2025-04-25"),
        Estudiante(None, "Mónica Silva", 22, "Medicina", "monica.silva@example.com", "2025-04-26"),
        Estudiante(None, "Tomás Guzmán", 23, "Derecho", "tomas.guzman@example.com", "2025-04-27"),
        Estudiante(None, "Paula Vargas", 20, "Arquitectura", "paula.vargas@example.com", "2025-04-28"),
        Estudiante(None, "Ignacio Fuentes", 24, "Economía", "ignacio.fuentes@example.com", "2025-04-29"),
        Estudiante(None, "Mariana León", 19, "Psicología", "mariana.leon@example.com", "2025-04-30"),
    ]

    for estudiante in estudiantes:
        resultado = servicio.insertar(estudiante)
        if resultado:
            print(f"✅ Estudiante '{estudiante.nombre}' insertado correctamente.")
        else:
            print(f"❌ No se pudo insertar el estudiante '{estudiante.nombre}'.")

if __name__ == "__main__":
    insertar_estudiantes_masivamente()