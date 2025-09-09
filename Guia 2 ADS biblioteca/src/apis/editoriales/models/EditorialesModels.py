from database.database import get_connection
from ..models.entities.Editoriales import Editorial
from psycopg2.extras import DictCursor

class EditorialModel:
    
    @classmethod
    def get_all(cls):
        connection = get_connection()
        try:
            with connection.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute("SELECT * FROM editoriales ORDER BY nombre")
                return [Editorial(*row).to_JSON() for row in cursor.fetchall()]
        finally:
            connection.close()

    @classmethod
    def get_by_id(cls, id):
        connection = get_connection()
        try:
            with connection.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute("SELECT * FROM editoriales WHERE id = %s", (id,))
                row = cursor.fetchone()
                return Editorial(*row).to_JSON() if row else None
        finally:
            connection.close()

    @classmethod
    def add(cls, editorial):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO editoriales (id, nombre) VALUES (%s, %s)
                """, (editorial.id, editorial.nombre))
                connection.commit()
                return cursor.rowcount
        except:
            connection.rollback()
            raise
        finally:
            connection.close()

    @classmethod
    def update(cls, editorial):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE editoriales SET nombre = %s WHERE id = %s
                """, (editorial.nombre, editorial.id))
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
                cursor.execute("DELETE FROM editoriales WHERE id = %s", (id,))
                connection.commit()
                return cursor.rowcount
        except:
            connection.rollback()
            raise
        finally:
            connection.close()