import uuid
from datetime import datetime

class Auditoria:
    def __init__(self, id=None, id_libro=None, fecha=None, accion=None, usuario=None):
        self.id = id or str(uuid.uuid4())
        self.id_libro = id_libro
        self.fecha = fecha or datetime.now()
        self.accion = accion
        self.usuario = usuario

    def to_JSON(self):
        return {
            "id": self.id,
            "id_libro": self.id_libro,
            "fecha": self.fecha.isoformat(),
            "accion": self.accion,
            "usuario": self.usuario
        }