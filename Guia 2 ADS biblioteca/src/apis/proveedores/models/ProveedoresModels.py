from database.database import get_connection
from ..models.entities.Proveedores import Proveedor
from psycopg2.extras import DictCursor

class ProveedorModel:
    
    @classmethod
    def get_all(cls):
        connection = get_connection()
        try:
            with connection.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute("SELECT * FROM proveedores ORDER BY nombre")
                return [Proveedor(*row).to_JSON() for row in cursor.fetchall()]
        finally:
            connection.close()

    @classmethod
    def get_by_id(cls, id):
        connection = get_connection()
        try:
            with connection.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute("SELECT * FROM proveedores WHERE id = %s", (id,))
                row = cursor.fetchone()
                return Proveedor(*row).to_JSON() if row else None
        finally:
            connection.close()

    @classmethod
    def add(cls, proveedor):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO proveedores (id, nombre, contacto) 
                    VALUES (%s, %s, %s)
                """, (proveedor.id, proveedor.nombre, proveedor.contacto))
                connection.commit()
                return cursor.rowcount
        except:
            connection.rollback()
            raise
        finally:
            connection.close()

    @classmethod
    def update(cls, proveedor):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE proveedores SET
                        nombre = %s,
                        contacto = %s
                    WHERE id = %s
                """, (proveedor.nombre, proveedor.contacto, proveedor.id))
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
                cursor.execute("DELETE FROM proveedores WHERE id = %s", (id,))
                connection.commit()
                return cursor.rowcount
        except:
            connection.rollback()
            raise
        finally:
            connection.close()