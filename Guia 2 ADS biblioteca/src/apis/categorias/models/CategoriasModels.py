from database.database import get_connection
from ..models.entities.Categorias import Categoria
from psycopg2.extras import DictCursor

class CategoriaModel:
    
    @classmethod
    def get_all(cls):
        connection = get_connection()
        try:
            with connection.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute("SELECT * FROM categorias ORDER BY nombre")
                return [Categoria(*row).to_JSON() for row in cursor.fetchall()]
        finally:
            connection.close()

    @classmethod
    def get_by_id(cls, id):
        connection = get_connection()
        try:
            with connection.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute("SELECT * FROM categorias WHERE id = %s", (id,))
                row = cursor.fetchone()
                return Categoria(*row).to_JSON() if row else None
        finally:
            connection.close()

    @classmethod
    def add(cls, categoria):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO categorias (id, nombre) VALUES (%s, %s)
                """, (categoria.id, categoria.nombre))
                connection.commit()
                return cursor.rowcount
        except:
            connection.rollback()
            raise
        finally:
            connection.close()

    @classmethod
    def update(cls, categoria):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE categorias SET nombre = %s WHERE id = %s
                """, (categoria.nombre, categoria.id))
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
                cursor.execute("DELETE FROM categorias WHERE id = %s", (id,))
                connection.commit()
                return cursor.rowcount
        except:
            connection.rollback()
            raise
        finally:
            connection.close()