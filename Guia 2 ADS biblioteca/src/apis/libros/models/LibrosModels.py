from database.database import get_connection
from ..models.entities.Libros import Libro
from psycopg2.extras import DictCursor

class LibroModel:
    
    @classmethod
    def get_all(cls):
        connection = get_connection()
        try:
            with connection.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute("SELECT * FROM libros ORDER BY titulo")
                return [Libro(*row).to_JSON() for row in cursor.fetchall()]
        finally:
            connection.close()

    @classmethod
    def get_by_id(cls, id):
        connection = get_connection()
        try:
            with connection.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute("SELECT * FROM libros WHERE id = %s", (id,))
                row = cursor.fetchone()
                return Libro(*row).to_JSON() if row else None
        finally:
            connection.close()

    @classmethod
    def add(cls, libro):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO libros (
                        id, titulo, id_autor, id_editorial, 
                        id_categoria, id_ubicacion, fecha_publicacion, isbn
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    libro.id, libro.titulo, libro.id_autor, libro.id_editorial,
                    libro.id_categoria, libro.id_ubicacion, 
                    libro.fecha_publicacion, libro.isbn
                ))
                connection.commit()
                return cursor.rowcount
        except:
            connection.rollback()
            raise
        finally:
            connection.close()

    @classmethod
    def update(cls, libro):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE libros SET
                        titulo = %s,
                        id_autor = %s,
                        id_editorial = %s,
                        id_categoria = %s,
                        id_ubicacion = %s,
                        fecha_publicacion = %s,
                        isbn = %s
                    WHERE id = %s
                """, (
                    libro.titulo, libro.id_autor, libro.id_editorial,
                    libro.id_categoria, libro.id_ubicacion,
                    libro.fecha_publicacion, libro.isbn,
                    libro.id
                ))
                connection.commit()
                return cursor.rowcount
        except:
            connection.rollback()
            raise
        finally:
            connection.close()

    @classmethod
    def delete(cls, id):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM libros WHERE id = %s", (id,))
                connection.commit()
                return cursor.rowcount
        except:
            connection.rollback()
            raise
        finally:
            connection.close()