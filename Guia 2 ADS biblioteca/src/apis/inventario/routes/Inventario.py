from flask import Blueprint, jsonify, request
from ..models.InventariosModels import InventarioModel
from ..models.entities.Inventarios import Inventario
from services.twilio_service import enviar_whatsapp
import uuid
import psycopg2
from database.database import get_connection

main = Blueprint("inventario_blueprint", __name__)

@main.route('/', methods=['GET'])
def get_inventario():
    try:
        inventario = InventarioModel.get_all()
        return jsonify({
            "success": True,
            "message": "Lista de inventario",
            "data": inventario,
            "count": len(inventario)
        }), 200
    except Exception as ex:
        return jsonify({"success": False, "error": str(ex)}), 500

@main.route('/<id>', methods=['GET'])
def get_item_inventario(id):
    try:
        item = InventarioModel.get_by_id(id)
        if item:
            return jsonify({"success": True, "message": "Ítem de inventario encontrado", "data": item}), 200
        return jsonify({"success": False, "message": "Ítem de inventario no encontrado"}), 404
    except Exception as ex:
        return jsonify({"success": False, "error": str(ex)}), 500

@main.route('/add', methods=['POST'])
def add_item_inventario():
    try:
        data = request.get_json()
        
        required_fields = ['id_libro', 'cantidad', 'id_proveedor']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                "success": False,
                "error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"
            }), 400

        item = Inventario(
            id=str(uuid.uuid4()),
            id_libro=data['id_libro'],
            cantidad=data['cantidad'],
            id_proveedor=data['id_proveedor']
        )
        
        affected_rows = InventarioModel.add(item)
        if affected_rows == 1:
            # ✅ Obtener título del libro
            conn = get_connection()
            with conn.cursor() as cursor:
                cursor.execute("SELECT titulo FROM libros WHERE id = %s", (item.id_libro,))
                resultado = cursor.fetchone()
                titulo = resultado[0] if resultado else "Libro desconocido"
            conn.close()
            
            # ✅ Enviar notificación por WhatsApp
            mensaje = f"📚 Se han añadido {item.cantidad} unidades del libro '{titulo}' al inventario."
            enviar_whatsapp("+50377523537", mensaje)  # ✅ Número de prueba o configurable
            
            return jsonify({
                "success": True,
                "message": "Ítem de inventario registrado y notificado",
                "id": item.id
            }), 201
            
        return jsonify({"success": False, "error": "No se pudo registrar"}), 400
    except Exception as ex:
        return jsonify({"success": False, "error": str(ex)}), 500

@main.route('/update/<id>', methods=['PUT'])
def update_item_inventario(id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "Datos requeridos"}), 400

        item = Inventario(
            id=id,
            id_libro=data.get('id_libro'),
            cantidad=data.get('cantidad'),
            id_proveedor=data.get('id_proveedor')
        )
        
        affected_rows = InventarioModel.update(item)
        if affected_rows == 1:
            return jsonify({"success": True, "message": "Ítem de inventario actualizado"}), 200
        return jsonify({"success": False, "error": "No se actualizó"}), 400
    except Exception as ex:
        return jsonify({"success": False, "error": str(ex)}), 500

@main.route('/delete/<id>', methods=['DELETE'])
def delete_item_inventario(id):
    try:
        affected_rows = InventarioModel.delete(id)
        if affected_rows == 1:
            return jsonify({"success": True, "message": "Ítem de inventario eliminado"}), 200
        return jsonify({"success": False, "error": "No se eliminó"}), 400
    except Exception as ex:
        return jsonify({"success": False, "error": str(ex)}), 500