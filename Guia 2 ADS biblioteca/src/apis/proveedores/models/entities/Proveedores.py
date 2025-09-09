import uuid

class Proveedor:
    def __init__(self, id=None, nombre=None, contacto=None):
        self.id = id or str(uuid.uuid4())
        self.nombre = nombre
        self.contacto = contacto

    def to_JSON(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "contacto": self.contacto
        }