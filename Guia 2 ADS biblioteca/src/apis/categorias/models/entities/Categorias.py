import uuid

class Categoria:
    def __init__(self, id=None, nombre=None):
        self.id = id or str(uuid.uuid4())
        self.nombre = nombre

    def to_JSON(self):
        return {
            "id": self.id,
            "nombre": self.nombre
        }