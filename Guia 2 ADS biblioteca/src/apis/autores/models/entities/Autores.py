import uuid


class Autor:
    def __init__(self, id=None, nombre=None, apellido=None, fecha_nacimiento=None, nacionalidad=None):
        self.id = id or str(uuid.uuid4())
        self.nombre = nombre
        self.apellido = apellido
        self.fecha_nacimiento = fecha_nacimiento
        self.nacionalidad = nacionalidad

    def to_JSON(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "fecha_nacimiento": str(self.fecha_nacimiento) if self.fecha_nacimiento else None,
            "nacionalidad": self.nacionalidad
        }