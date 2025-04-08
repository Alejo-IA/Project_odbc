**Documentación del Proyecto CRUD de Estudiantes con ODBC y PostgreSQL**

# 1. Introducción
Este proyecto consiste en un sistema CRUD (Crear, Leer, Actualizar y Eliminar) de estudiantes utilizando Python, ODBC y PostgreSQL. La interfaz gráfica está construida con Tkinter, permitiendo una gestión intuitiva de la base de datos de estudiantes.

# 2. Tecnologías Utilizadas
- **Python 3.13**: Lenguaje de programación principal.
- **ODBC**: Controlador para conectar con PostgreSQL.
- **PostgreSQL**: Base de datos relacional.
- **Tkinter**: Para la interfaz gráfica.
- **psycopg2**: Biblioteca para interactuar con PostgreSQL.

# 3. Estructura del Proyecto
El proyecto está organizado en los siguientes directorios y archivos:

```
PROYECTO_ODBC/
│── .venv/                 # Entorno virtual de Python
│── config/                # Configuraciones generales
│   ├── odbc_config.py     # Configuración de la conexión a la BD
│── database/              # Scripts relacionados con la base de datos
│── models/                # Modelos de datos
│── services/              # Servicios de negocio
│── main.py                # Punto de entrada del programa
│── requirements.txt       # Dependencias del proyecto
│── README.md              # Documentación general
```

# 4. Configuración de la Base de Datos
La base de datos debe ser configurada en PostgreSQL antes de ejecutar el proyecto. Se incluyen scripts para la creación automática de la base de datos y la tabla correspondiente.

## 4.1. Variables de Entorno
En el archivo `config/odbc_config.py`, se definen los valores de conexión a la base de datos:
```python
self.host = os.getenv('DB_HOST', 'localhost')
self.database = os.getenv('DB_NAME', 'universidad')
self.user = os.getenv('DB_USER', 'postgres')
self.password = os.getenv('DB_PASSWORD', 'tu_contraseña')
```

# 5. Funcionalidades Principales
- **Crear**: Agregar un nuevo estudiante a la base de datos.
- **Leer**: Mostrar la lista de estudiantes registrados.
- **Actualizar**: Modificar la información de un estudiante.
- **Eliminar**: Borrar un estudiante de la base de datos.

# 6. Ejecución del Proyecto
## 6.1. Instalación de Dependencias
Antes de ejecutar el proyecto, es necesario instalar las dependencias:
```sh
pip install -r requirements.txt
```

## 6.2. Creación de la Base de Datos
Ejecutar el script que crea la base de datos y la tabla:
```sh
python -c "from config.odbc_config import crear_base_de_datos_y_tabla; crear_base_de_datos_y_tabla()"
```

## 6.3. Iniciar la Aplicación
```sh
python main.py
```

# 7. Conclusión
Este proyecto proporciona una base sólida para la gestión de estudiantes en PostgreSQL mediante Python y ODBC. Su estructura modular permite escalabilidad y mantenimiento fácil.
