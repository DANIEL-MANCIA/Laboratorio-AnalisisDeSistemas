from database.database import get_connection
from ..models.entities.Auditorias import Auditoria
from psycopg2.extras import DictCursor

class AuditoriaModel:
    
    @classmethod
    def get_all(cls):
        connection = get_connection()
        try:
            with connection.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute("SELECT * FROM auditorias ORDER BY fecha DESC")
                return [Auditoria(*row).to_JSON() for row in cursor.fetchall()]
        finally:
            connection.close()

    @classmethod
    def get_by_id(cls, id):
        connection = get_connection()
        try:
            with connection.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute("SELECT * FROM auditorias WHERE id = %s", (id,))
                row = cursor.fetchone()
                return Auditoria(*row).to_JSON() if row else None
        finally:
            connection.close()

    @classmethod
    def get_by_libro(cls, id_libro):
        connection = get_connection()
        try:
            with connection.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute("SELECT * FROM auditorias WHERE id_libro = %s ORDER BY fecha DESC", (id_libro,))
                return [Auditoria(*row).to_JSON() for row in cursor.fetchall()]
        finally:
            connection.close()

    @classmethod
    def add(cls, auditoria):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO auditorias (
                        id, id_libro, fecha, accion, usuario
                    ) VALUES (%s, %s, %s, %s, %s)
                """, (
                    auditoria.id, auditoria.id_libro, 
                    auditoria.fecha, auditoria.accion, 
                    auditoria.usuario
                ))
                connection.commit()
                return cursor.rowcount
        except:
            connection.rollback()
            raise
        finally:
            connection.close()

    @classmethod
    def update(cls, auditoria):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE auditorias 
                    SET id_libro = %s, accion = %s, usuario = %s
                    WHERE id = %s
                """, (
                    auditoria.id_libro,
                    auditoria.accion,
                    auditoria.usuario,
                    auditoria.id
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
                cursor.execute("DELETE FROM auditorias WHERE id = %s", (id,))
                connection.commit()
                return cursor.rowcount
        except:
            connection.rollback()
            raise
        finally:
            connection.close()

