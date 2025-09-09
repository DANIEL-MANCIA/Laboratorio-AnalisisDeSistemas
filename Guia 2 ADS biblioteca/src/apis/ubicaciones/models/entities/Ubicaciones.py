import uuid

class Ubicacion:
    def __init__(self, id=None, sala=None, pasillo=None, estanteria=None, seccion=None):
        self.id = id or str(uuid.uuid4())
        self.sala = sala
        self.pasillo = pasillo
        self.estanteria = estanteria
        self.seccion = seccion

    def to_JSON(self):
        return {
            "id": self.id,
            "sala": self.sala,
            "pasillo": self.pasillo,
            "estanteria": self.estanteria,
            "seccion": self.seccion
        }