import uuid

class Inventario:
    def __init__(self, id=None, id_libro=None, cantidad=None, id_proveedor=None):
        self.id = id or str(uuid.uuid4())
        self.id_libro = id_libro
        self.cantidad = cantidad
        self.id_proveedor = id_proveedor

    def to_JSON(self):
        return {
            "id": self.id,
            "id_libro": self.id_libro,
            "cantidad": self.cantidad,
            "id_proveedor": self.id_proveedor
        }