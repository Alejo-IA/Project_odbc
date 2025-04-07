class Estudiante:
    def __init__(self, id=None, nombre=None, edad=None, carrera=None, correo=None, fecha_ingreso=None):
        self.id = id
        self.nombre = nombre
        self.edad = edad
        self.carrera = carrera
        self.correo = correo
        self.fecha_ingreso = fecha_ingreso

    def to_tuple(self):
        """Convierte el objeto Estudiante a una tupla para su inserción en la base de datos"""
        return (self.id, self.nombre, self.edad, self.carrera, self.correo, self.fecha_ingreso)

    @classmethod
    def from_tuple(cls, data):
        """Crea un objeto Estudiante a partir de una tupla extraída de la base de datos"""
        return cls(*data)

    def __repr__(self):
        """Representación en string para depuración"""
        return f"Estudiante(id={self.id}, nombre='{self.nombre}', edad={self.edad}, carrera='{self.carrera}', correo='{self.correo}', fecha_ingreso={self.fecha_ingreso})"