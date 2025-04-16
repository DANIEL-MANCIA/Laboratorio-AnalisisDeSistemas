from database.database import get_connection
from ..models.entities.Inventarios import Inventario
from psycopg2.extras import DictCursor

class InventarioModel:
    
    @classmethod
    def get_all(cls):
        connection = get_connection()
        try:
            with connection.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute("SELECT * FROM inventario")
                return [Inventario(*row).to_JSON() for row in cursor.fetchall()]
        finally:
            connection.close()

    @classmethod
    def get_by_id(cls, id):
        connection = get_connection()
        try:
            with connection.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute("SELECT * FROM inventario WHERE id = %s", (id,))
                row = cursor.fetchone()
                return Inventario(*row).to_JSON() if row else None
        finally:
            connection.close()

    @classmethod
    def add(cls, inventario):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO inventario (
                        id, id_libro, cantidad, id_proveedor
                    ) VALUES (%s, %s, %s, %s)
                """, (
                    inventario.id, inventario.id_libro, 
                    inventario.cantidad, inventario.id_proveedor
                ))
                connection.commit()
                return cursor.rowcount
        except:
            connection.rollback()
            raise
        finally:
            connection.close()

    @classmethod
    def update(cls, inventario):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE inventario SET
                        id_libro = %s,
                        cantidad = %s,
                        id_proveedor = %s
                    WHERE id = %s
                """, (
                    inventario.id_libro, inventario.cantidad, 
                    inventario.id_proveedor, inventario.id
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
                cursor.execute("DELETE FROM inventario WHERE id = %s", (id,))
                connection.commit()
                return cursor.rowcount
        except:
            connection.rollback()
            raise
        finally:
            connection.close()