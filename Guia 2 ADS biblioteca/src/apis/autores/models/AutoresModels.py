from database.database import get_connection
from ..models.entities.Autores import Autor
from psycopg2.extras import DictCursor

class AutorModel:
    
    @classmethod
    def get_all(cls):
        connection = get_connection()
        try:
            with connection.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute("SELECT * FROM autores ORDER BY nombre")
                return [Autor(*row).to_JSON() for row in cursor.fetchall()]
        finally:
            connection.close()

    @classmethod
    def get_by_id(cls, id):
        connection = get_connection()
        try:
            with connection.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute("SELECT * FROM autores WHERE id = %s", (id,))
                row = cursor.fetchone()
                return Autor(*row).to_JSON() if row else None
        finally:
            connection.close()

    @classmethod
    def add(cls, autor):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO autores (
                        id, nombre, apellido, fecha_nacimiento, nacionalidad
                    ) VALUES (%s, %s, %s, %s, %s)
                """, (
                    autor.id, autor.nombre, autor.apellido, 
                    autor.fecha_nacimiento, autor.nacionalidad
                ))
                connection.commit()
                return cursor.rowcount
        except:
            connection.rollback()
            raise
        finally:
            connection.close()

    @classmethod
    def update(cls, autor):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE autores SET
                        nombre = %s,
                        apellido = %s,
                        fecha_nacimiento = %s,
                        nacionalidad = %s
                    WHERE id = %s
                """, (
                    autor.nombre, autor.apellido, 
                    autor.fecha_nacimiento, autor.nacionalidad,
                    autor.id
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
                cursor.execute("DELETE FROM autores WHERE id = %s", (id,))
                connection.commit()
                return cursor.rowcount
        except:
            connection.rollback()
            raise
        finally:
            connection.close()