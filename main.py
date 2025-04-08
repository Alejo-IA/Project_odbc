import tkinter as tk
from tkinter import Menu, filedialog, messagebox
from tkinter import ttk  # Importar ttk para usar Treeview
from tkcalendar import DateEntry
import csv
from config.odbc_config import DatabaseConfig, crear_base_de_datos_y_tabla
from services.database_service import EstudianteService
from models.estudiante import Estudiante


class EstudianteApp:
    def __init__(self, master, servicio):
        self.master = master
        self.servicio = servicio
        master.title("Sistema de Gestión de Estudiantes")
        master.geometry("1100x700")

        # Menú superior
        self.menu = Menu(master)
        master.config(menu=self.menu)
        self.menu.add_command(label="Acerca de", command=self.mostrar_acerca_de)
        self.menu.add_command(label="Salir", command=master.quit)

        # Frame principal
        self.frame_principal = tk.Frame(master)
        self.frame_principal.pack(padx=20, pady=20, fill="both", expand=True)

        # Frame para búsqueda
        self.frame_busqueda = tk.Frame(master)
        self.frame_busqueda.pack(pady=10)

        tk.Label(self.frame_busqueda, text="Buscar:").pack(side="left", padx=5)
        self.entry_busqueda = ttk.Entry(self.frame_busqueda)
        self.entry_busqueda.pack(side="left", padx=5)
        self.entry_busqueda.bind("<KeyRelease>", self.buscar_estudiantes)

        # Frame para filtro por carrera
        self.frame_filtro = tk.Frame(master)
        self.frame_filtro.pack(pady=10)

        tk.Label(self.frame_filtro, text="Filtrar por Carrera:").pack(side="left", padx=5)
        self.combobox_carrera = ttk.Combobox(self.frame_filtro, state="readonly", width=30)
        self.combobox_carrera.pack(side="left", padx=5)
        self.combobox_carrera.bind("<<ComboboxSelected>>", self.filtrar_por_carrera)

        # Frame para botones
        self.frame_botones = tk.Frame(master)
        self.frame_botones.pack(pady=10)

        self.btn_agregar = ttk.Button(self.frame_botones, text="Agregar Estudiante", command=self.agregar_estudiante)
        self.btn_agregar.pack(side="left", padx=5)

        self.btn_editar = ttk.Button(self.frame_botones, text="Editar Estudiante", command=self.editar_estudiante)
        self.btn_editar.pack(side="left", padx=5)

        self.btn_eliminar = ttk.Button(self.frame_botones, text="Eliminar Estudiante", command=self.eliminar_estudiante)
        self.btn_eliminar.pack(side="left", padx=5)

        self.btn_actualizar = ttk.Button(self.frame_botones, text="Actualizar", command=self.cargar_estudiantes)
        self.btn_actualizar.pack(side="left", padx=5)

        self.btn_exportar = ttk.Button(self.frame_botones, text="Exportar a CSV", command=self.exportar_csv)
        self.btn_exportar.pack(side="left", padx=5)

        self.btn_importar = ttk.Button(self.frame_botones, text="Importar desde CSV", command=self.importar_csv)
        self.btn_importar.pack(side="left", padx=5)

        # Crear tabla
        self.crear_tabla()

        # Frame para estadísticas
        self.frame_estadisticas = tk.Frame(master)
        self.frame_estadisticas.pack(pady=10)

        self.label_total_estudiantes = tk.Label(self.frame_estadisticas, text="Total de Estudiantes: 0")
        self.label_total_estudiantes.pack(side="left", padx=10)

        self.label_promedio_edad = tk.Label(self.frame_estadisticas, text="Promedio de Edad: 0")
        self.label_promedio_edad.pack(side="left", padx=10)

        self.label_estudiantes_por_carrera = tk.Label(self.frame_estadisticas, text="Estudiantes por Carrera: 0")
        self.label_estudiantes_por_carrera.pack(side="left", padx=10)

        # Barra de estado
        self.status_bar = tk.Label(master, text="Conectado a la base de datos mediante ODBC", anchor="w", relief="sunken")
        self.status_bar.pack(side="bottom", fill="x")

        # Cargar datos iniciales
        self.cargar_estudiantes()
        self.cargar_carreras()
        self.actualizar_estadisticas()

    def crear_tabla(self):
        columnas = ("ID", "Nombre", "Edad", "Carrera", "Correo", "Fecha de Ingreso")
        self.tabla = ttk.Treeview(self.frame_principal, columns=columnas, show="headings", height=20)
        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, anchor="center", width=150)
        self.tabla.pack(fill="both", expand=True)

    def cargar_estudiantes(self):
        for row in self.tabla.get_children():
            self.tabla.delete(row)

        estudiantes = self.servicio.obtener_todos()
        for estudiante in estudiantes:
            self.tabla.insert("", "end", values=(estudiante.id, estudiante.nombre, estudiante.edad, estudiante.carrera, estudiante.correo, estudiante.fecha_ingreso))

    def buscar_estudiantes(self, event=None):
        texto_busqueda = self.entry_busqueda.get().lower()
        for row in self.tabla.get_children():
            self.tabla.delete(row)

        estudiantes = self.servicio.obtener_todos()
        for estudiante in estudiantes:
            if (
                texto_busqueda in str(estudiante.nombre).lower()
                or texto_busqueda in str(estudiante.carrera).lower()
                or texto_busqueda in str(estudiante.correo).lower()
                or texto_busqueda in str(estudiante.fecha_ingreso).lower()
            ):
                self.tabla.insert("", "end", values=(estudiante.id, estudiante.nombre, estudiante.edad, estudiante.carrera, estudiante.correo, estudiante.fecha_ingreso))

    def cargar_carreras(self):
        estudiantes = self.servicio.obtener_todos()
        carreras = sorted(set(estudiante.carrera for estudiante in estudiantes))
        self.combobox_carrera["values"] = ["Todas"] + carreras
        self.combobox_carrera.set("Todas")

    def filtrar_por_carrera(self, event=None):
        carrera_seleccionada = self.combobox_carrera.get()
        for row in self.tabla.get_children():
            self.tabla.delete(row)

        estudiantes = self.servicio.obtener_todos()
        for estudiante in estudiantes:
            if carrera_seleccionada == "Todas" or estudiante.carrera == carrera_seleccionada:
                self.tabla.insert("", "end", values=(estudiante.id, estudiante.nombre, estudiante.edad, estudiante.carrera, estudiante.correo, estudiante.fecha_ingreso))

    def actualizar_estadisticas(self):
        estudiantes = self.servicio.obtener_todos()
        total_estudiantes = len(estudiantes)
        promedio_edad = sum(estudiante.edad for estudiante in estudiantes) / total_estudiantes if total_estudiantes > 0 else 0
        estudiantes_por_carrera = len(set(estudiante.carrera for estudiante in estudiantes))

        self.label_total_estudiantes.config(text=f"Total de Estudiantes: {total_estudiantes}")
        self.label_promedio_edad.config(text=f"Promedio de Edad: {promedio_edad:.2f}")
        self.label_estudiantes_por_carrera.config(text=f"Estudiantes por Carrera: {estudiantes_por_carrera}")

    def agregar_estudiante(self):
        ventana = tk.Toplevel(self.master)
        ventana.title("Agregar Estudiante")
        ventana.geometry("400x400")

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
        entry_fecha = DateEntry(ventana, date_pattern="yyyy-MM-dd")
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
            if self.servicio.insertar(nuevo_estudiante):
                messagebox.showinfo("Éxito", "Estudiante agregado correctamente")
                self.cargar_estudiantes()
                self.actualizar_estadisticas()
                ventana.destroy()
            else:
                messagebox.showerror("Error", "No se pudo agregar el estudiante")

        ttk.Button(ventana, text="Guardar", command=confirmar_agregar).pack(pady=20)

    def editar_estudiante(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un estudiante para editar")
            return
        item = self.tabla.item(seleccion)
        estudiante_id = item["values"][0]
        estudiante = self.servicio.obtener_por_id(estudiante_id)

        ventana = tk.Toplevel(self.master)
        ventana.title("Editar Estudiante")
        ventana.geometry("400x400")

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
        entry_fecha = DateEntry(ventana, date_pattern="yyyy-MM-dd")
        entry_fecha.pack()
        entry_fecha.set_date(estudiante.fecha_ingreso)

        def confirmar_editar():
            estudiante.nombre = entry_nombre.get()
            estudiante.edad = int(entry_edad.get())
            estudiante.carrera = entry_carrera.get()
            estudiante.correo = entry_correo.get()
            estudiante.fecha_ingreso = entry_fecha.get()

            if self.servicio.actualizar(estudiante):
                messagebox.showinfo("Éxito", "Estudiante actualizado correctamente")
                self.cargar_estudiantes()
                self.actualizar_estadisticas()
                ventana.destroy()
            else:
                messagebox.showerror("Error", "No se pudo actualizar el estudiante")

        ttk.Button(ventana, text="Guardar", command=confirmar_editar).pack(pady=20)

    def eliminar_estudiante(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un estudiante para eliminar")
            return
        item = self.tabla.item(seleccion)
        estudiante_id = item["values"][0]

        if messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar este estudiante?"):
            if self.servicio.eliminar(estudiante_id):
                messagebox.showinfo("Éxito", "Estudiante eliminado correctamente")
                self.cargar_estudiantes()
                self.actualizar_estadisticas()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el estudiante")

    def exportar_csv(self):
        """Exportar estudiantes a un archivo CSV."""
        # Abrir cuadro de diálogo para guardar el archivo
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Guardar archivo CSV"
        )
        if not file_path:
            return  # Si el usuario cancela, no hacer nada

        # Obtener los estudiantes de la base de datos
        estudiantes = self.servicio.obtener_todos()
        if not estudiantes:
            messagebox.showwarning("Advertencia", "No hay datos para exportar.")
            return

        try:
            # Escribir los datos en el archivo CSV
            with open(file_path, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                # Escribir encabezados
                writer.writerow(["ID", "Nombre", "Edad", "Carrera", "Correo", "Fecha de Ingreso"])
                # Escribir datos de los estudiantes
                for estudiante in estudiantes:
                    writer.writerow([
                        estudiante.id,
                        estudiante.nombre,
                        estudiante.edad,
                        estudiante.carrera,
                        estudiante.correo,
                        estudiante.fecha_ingreso
                    ])
            messagebox.showinfo("Exportar CSV", f"Estudiantes exportados correctamente a {file_path}.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar el archivo CSV: {e}")
    def importar_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return

        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                nuevo_estudiante = Estudiante(
                    None,
                    row["Nombre"],
                    int(row["Edad"]),
                    row["Carrera"],
                    row["Correo"],
                    row["Fecha de Ingreso"],
                )
                self.servicio.insertar(nuevo_estudiante)

        self.cargar_estudiantes()
        self.actualizar_estadisticas()
        messagebox.showinfo("Importar CSV", "Estudiantes importados correctamente.")

    def mostrar_acerca_de(self):
        messagebox.showinfo("Acerca de", "Sistema de Gestión de Estudiantes\nUsando ODBC y PostgreSQL")


def main():
    try:
        db_config = DatabaseConfig()
        conn = db_config.get_connection()
        if conn:
            db_config.release_connection(conn)
            crear_base_de_datos_y_tabla()
        else:
            print("Error: No se pudo conectar a la base de datos.")
            return

        root = tk.Tk()
        servicio_estudiantes = EstudianteService(db_config)
        app = EstudianteApp(root, servicio_estudiantes)
        root.mainloop()

    except Exception as e:
        print(f"Error en la aplicación: {e}")


if __name__ == "__main__":
    main()