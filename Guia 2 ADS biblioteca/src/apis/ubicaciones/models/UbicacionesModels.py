from database.database import get_connection
from ..models.entities.Ubicaciones import Ubicacion
from psycopg2.extras import DictCursor

class UbicacionModel:
    
    @classmethod
    def get_all(cls):
        connection = get_connection()
        try:
            with connection.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute("SELECT * FROM ubicaciones")
                return [Ubicacion(*row).to_JSON() for row in cursor.fetchall()]
        finally:
            connection.close()

    @classmethod
    def get_by_id(cls, id):
        connection = get_connection()
        try:
            with connection.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute("SELECT * FROM ubicaciones WHERE id = %s", (id,))
                row = cursor.fetchone()
                return Ubicacion(*row).to_JSON() if row else None
        finally:
            connection.close()

    @classmethod
    def add(cls, ubicacion):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO ubicaciones (
                        id, sala, pasillo, estanteria, seccion
                    ) VALUES (%s, %s, %s, %s, %s)
                """, (
                    ubicacion.id, ubicacion.sala, ubicacion.pasillo,
                    ubicacion.estanteria, ubicacion.seccion
                ))
                connection.commit()
                return cursor.rowcount
        except:
            connection.rollback()
            raise
        finally:
            connection.close()

    @classmethod
    def update(cls, ubicacion):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE ubicaciones SET
                        sala = %s,
                        pasillo = %s,
                        estanteria = %s,
                        seccion = %s
                    WHERE id = %s
                """, (
                    ubicacion.sala, ubicacion.pasillo,
                    ubicacion.estanteria, ubicacion.seccion,
                    ubicacion.id
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
                cursor.execute("DELETE FROM ubicaciones WHERE id = %s", (id,))
                connection.commit()
                return cursor.rowcount
        except:
            connection.rollback()
            raise
        finally:
            connection.close()