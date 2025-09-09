from flask import Blueprint, jsonify, request
from ..models.AuditoriasModels import AuditoriaModel
from ..models.entities.Auditorias import Auditoria
from services.twilio_service import enviar_whatsapp
from database.database import get_connection
import uuid

main = Blueprint("auditorias_blueprint", __name__)

@main.route('/', methods=['GET'])
def get_auditorias():
    try:
        auditorias = AuditoriaModel.get_all()
        return jsonify({
            "success": True,
            "message": "Lista de auditorías",
            "data": auditorias,
            "count": len(auditorias)
        }), 200
    except Exception as ex:
        return jsonify({"success": False, "error": str(ex)}), 500

@main.route('/<id>', methods=['GET'])
def get_auditoria(id):
    try:
        auditoria = AuditoriaModel.get_by_id(id)
        if auditoria:
            return jsonify({"success": True, "message": "Auditoría encontrada", "data": auditoria}), 200
        return jsonify({"success": False, "message": "Auditoría no encontrada"}), 404
    except Exception as ex:
        return jsonify({"success": False, "error": str(ex)}), 500

@main.route('/libro/<id_libro>', methods=['GET'])
def get_auditorias_libro(id_libro):
    try:
        auditorias = AuditoriaModel.get_by_libro(id_libro)
        return jsonify({
            "success": True,
            "message": "Auditorías del libro",
            "data": auditorias,
            "count": len(auditorias)
        }), 200
    except Exception as ex:
        return jsonify({"success": False, "error": str(ex)}), 500

@main.route('/add', methods=['POST'])
def add_auditoria():
    try:
        data = request.get_json()
        
        required_fields = ['id_libro', 'accion', 'usuario']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                "success": False,
                "error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"
            }), 400

        auditoria = Auditoria(
            id=str(uuid.uuid4()),
            id_libro=data['id_libro'],
            accion=data['accion'],
            usuario=data['usuario']
        )
        
        affected_rows = AuditoriaModel.add(auditoria)
        if affected_rows == 1:
            # ✅ Obtener título del libro
            conn = get_connection()
            with conn.cursor() as cursor:
                cursor.execute("SELECT titulo FROM libros WHERE id = %s", (auditoria.id_libro,))
                resultado = cursor.fetchone()
                titulo = resultado[0] if resultado else "Libro desconocido"
            conn.close()

            # ✅ Enviar mensaje por WhatsApp
            mensaje = f"🕵️ Se ha registrado una acción: '{auditoria.accion}' sobre el libro '{titulo}' por el usuario {auditoria.usuario}."
            enviar_whatsapp("+50377523537", mensaje)  # Cambiar número si es necesario

            return jsonify({
                "success": True,
                "message": "Auditoría registrada y notificada",
                "id": auditoria.id
            }), 201
            
        return jsonify({"success": False, "error": "No se pudo registrar"}), 400
    except Exception as ex:
        return jsonify({"success": False, "error": str(ex)}), 500

@main.route('/<id>', methods=['PUT'])
def update_auditoria(id):
    try:
        data = request.get_json()
        required_fields = ['id_libro', 'accion', 'usuario']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                "success": False,
                "error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"
            }), 400

        auditoria = Auditoria(
            id=id,
            id_libro=data['id_libro'],
            accion=data['accion'],
            usuario=data['usuario']
        )

        affected_rows = AuditoriaModel.update(auditoria)
        if affected_rows == 1:
            return jsonify({
                "success": True,
                "message": "Auditoría actualizada correctamente",
                "id": auditoria.id
            }), 200

        return jsonify({"success": False, "message": "Auditoría no encontrada"}), 404
    except Exception as ex:
        return jsonify({"success": False, "error": str(ex)}), 500

@main.route('/<id>', methods=['DELETE'])
def delete_auditoria(id):
    try:
        auditoria = AuditoriaModel.get_by_id(id)
        if not auditoria:
            return jsonify({"success": False, "message": "Auditoría no encontrada"}), 404

        affected_rows = AuditoriaModel.delete(id)
        if affected_rows == 1:
            return jsonify({
                "success": True,
                "message": "Auditoría eliminada correctamente"
            }), 200

        return jsonify({"success": False, "message": "No se pudo eliminar"}), 400
    except Exception as ex:
        return jsonify({"success": False, "error": str(ex)}), 500