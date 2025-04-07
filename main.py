import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
from config.odbc_config import DatabaseConfig, crear_base_de_datos_y_tabla
from services.database_service import EstudianteService
from models.estudiante import Estudiante

class EstudianteApp:
    def __init__(self, master, servicio):
        self.master = master
        self.servicio = servicio
        master.title("Sistema de Gestión de Estudiantes")
        master.geometry("900x600")
        master.iconbitmap("icon.ico")  # Asegúrate de tener un archivo `icon.ico`

        # Menú superior
        self.menu = tk.Menu(master)
        master.config(menu=self.menu)
        self.menu.add_command(label="Acerca de", command=self.mostrar_acerca_de)
        self.menu.add_command(label="Salir", command=master.quit)

        # Frame principal
        self.frame_principal = tk.Frame(master)
        self.frame_principal.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Frame para botones
        self.frame_botones = tk.Frame(master)
        self.frame_botones.pack(pady=10)

        self.btn_agregar = ttk.Button(self.frame_botones, text="Agregar Estudiante", command=self.agregar_estudiante)
        self.btn_agregar.pack(side=tk.LEFT, padx=5)

        self.btn_editar = ttk.Button(self.frame_botones, text="Editar Estudiante", command=self.editar_estudiante)
        self.btn_editar.pack(side=tk.LEFT, padx=5)

        self.btn_eliminar = ttk.Button(self.frame_botones, text="Eliminar Estudiante", command=self.eliminar_estudiante)
        self.btn_eliminar.pack(side=tk.LEFT, padx=5)

        # Crear tabla
        self.crear_tabla()

        # Barra de estado
        self.status_bar = ttk.Label(master, text="Conectado a la base de datos mediante ODBC", relief=tk.SUNKEN, anchor="w")
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Cargar datos iniciales
        self.cargar_estudiantes()

    def crear_tabla(self):
        columnas = ("ID", "Nombre", "Edad", "Carrera", "Correo", "Fecha de Ingreso")
        self.tabla = ttk.Treeview(self.frame_principal, columns=columnas, show='headings', height=20)
        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, anchor="center", width=150)
        self.tabla.pack(fill=tk.BOTH, expand=True)

    def agregar_estudiante(self):
        ventana = tk.Toplevel(self.master)
        ventana.title("Agregar Estudiante")
        ventana.geometry("400x300")

        tk.Label(ventana, text="Nombre:").pack(pady=5)
        entry_nombre = ttk.Entry(ventana)
        entry_nombre.pack()

        tk.Label(ventana, text="Edad:").pack(pady=5)
        entry_edad = ttk.Entry(ventana)
        entry_edad.pack()

        tk.Label(ventana, text="Carrera:").pack(pady=5)
        entry_carrera = ttk.Entry(ventana)
        entry_carrera.pack()

        tk.Label(ventana, text="Correo:").pack(pady=5)
        entry_correo = ttk.Entry(ventana)
        entry_correo.pack()

        tk.Label(ventana, text="Fecha de Ingreso:").pack(pady=5)
        entry_fecha = DateEntry(ventana, date_pattern='yyyy-MM-dd')
        entry_fecha.pack()

        def confirmar_agregar():
            nombre = entry_nombre.get()
            edad = entry_edad.get()
            carrera = entry_carrera.get()
            correo = entry_correo.get()
            fecha_ingreso = entry_fecha.get()

            if not nombre or not edad or not carrera or not correo:
                messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")
                return

            try:
                edad = int(edad)
            except ValueError:
                messagebox.showerror("Error", "La edad debe ser un número")
                return

            nuevo_estudiante = Estudiante(None, nombre, edad, carrera, correo, fecha_ingreso)
            self.servicio.insertar(nuevo_estudiante)
            self.cargar_estudiantes()
            self.status_bar.config(text="Estudiante agregado correctamente")
            ventana.destroy()

        btn_guardar = ttk.Button(ventana, text="Guardar", command=confirmar_agregar)
        btn_guardar.pack(pady=10)

    def cargar_estudiantes(self):
        for row in self.tabla.get_children():
            self.tabla.delete(row)

        estudiantes = self.servicio.obtener_todos()
        for estudiante in estudiantes:
            self.tabla.insert("", tk.END, values=(estudiante.id, estudiante.nombre, estudiante.edad, estudiante.carrera, estudiante.correo, estudiante.fecha_ingreso))

    def editar_estudiante(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un estudiante para editar")
            return
        item = self.tabla.item(seleccion)
        estudiante_id = item['values'][0]
        estudiante = self.servicio.obtener_por_id(estudiante_id)

        ventana = tk.Toplevel(self.master)
        ventana.title("Editar Estudiante")
        ventana.geometry("400x300")

        tk.Label(ventana, text="Nombre:").pack(pady=5)
        entry_nombre = ttk.Entry(ventana)
        entry_nombre.pack()
        entry_nombre.insert(0, estudiante.nombre)

        tk.Label(ventana, text="Edad:").pack(pady=5)
        entry_edad = ttk.Entry(ventana)
        entry_edad.pack()
        entry_edad.insert(0, estudiante.edad)

        tk.Label(ventana, text="Carrera:").pack(pady=5)
        entry_carrera = ttk.Entry(ventana)
        entry_carrera.pack()
        entry_carrera.insert(0, estudiante.carrera)

        tk.Label(ventana, text="Correo:").pack(pady=5)
        entry_correo = ttk.Entry(ventana)
        entry_correo.pack()
        entry_correo.insert(0, estudiante.correo)

        tk.Label(ventana, text="Fecha de Ingreso:").pack(pady=5)
        entry_fecha = DateEntry(ventana, date_pattern='yyyy-MM-dd')
        entry_fecha.pack()
        entry_fecha.set_date(estudiante.fecha_ingreso)

        def confirmar_editar():
            estudiante.nombre = entry_nombre.get()
            estudiante.edad = int(entry_edad.get())
            estudiante.carrera = entry_carrera.get()
            estudiante.correo = entry_correo.get()
            estudiante.fecha_ingreso = entry_fecha.get()

            actualizado = self.servicio.actualizar(estudiante)
            if actualizado:
                self.cargar_estudiantes()
                self.status_bar.config(text="Estudiante actualizado correctamente")
                ventana.destroy()
            else:
                messagebox.showerror("Error", "No se pudo actualizar el estudiante")

        # Botón para guardar los cambios
        btn_guardar = ttk.Button(ventana, text="Guardar", command=confirmar_editar)
        btn_guardar.pack(pady=10)

    def eliminar_estudiante(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un estudiante para eliminar")
            return
        item = self.tabla.item(seleccion)
        estudiante_id = item['values'][0]

        self.servicio.eliminar(estudiante_id)
        self.cargar_estudiantes()
        self.status_bar.config(text="Estudiante eliminado correctamente")

    def mostrar_acerca_de(self):
        messagebox.showinfo("Acerca de", "Sistema de Gestión de Estudiantes\nUsando ODBC y PostgreSQL")

def main():
    try:
        # Configurar base de datos
        db_config = DatabaseConfig()
        conn = db_config.get_connection()
        if conn:
            db_config.release_connection(conn)
            crear_base_de_datos_y_tabla()
        else:
            print("Error: No se pudo conectar a la base de datos.")
            return

        # Crear ventana principal
        root = tk.Tk()
        servicio_estudiantes = EstudianteService(db_config)
        app = EstudianteApp(root, servicio_estudiantes)
        root.mainloop()

    except Exception as e:
        print(f"Error en la aplicación: {e}")

if __name__ == "__main__":
    main()