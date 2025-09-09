import uuid

class Libro:
    def __init__(self, id=None, titulo=None, id_autor=None, id_editorial=None, 
                 id_categoria=None, id_ubicacion=None, fecha_publicacion=None, isbn=None):
        self.id = id or str(uuid.uuid4())
        self.titulo = titulo
        self.id_autor = id_autor
        self.id_editorial = id_editorial
        self.id_categoria = id_categoria
        self.id_ubicacion = id_ubicacion
        self.fecha_publicacion = fecha_publicacion
        self.isbn = isbn

    def to_JSON(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "id_autor": self.id_autor,
            "id_editorial": self.id_editorial,
            "id_categoria": self.id_categoria,
            "id_ubicacion": self.id_ubicacion,
            "fecha_publicacion": str(self.fecha_publicacion) if self.fecha_publicacion else None,
            "isbn": self.isbn
        }