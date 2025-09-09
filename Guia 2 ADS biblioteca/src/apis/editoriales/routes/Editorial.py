from flask import Blueprint, jsonify, request
from ..models.EditorialesModels import EditorialModel
from ..models.entities.Editoriales import Editorial
import uuid

main = Blueprint("editoriales_blueprint", __name__)

@main.route('/', methods=['GET'])
def get_editoriales():
    try:
        editoriales = EditorialModel.get_all()
        return jsonify({
            "success": True,
            "message": "Lista de editoriales",
            "data": editoriales,
            "count": len(editoriales)
        }), 200
    except Exception as ex:
        return jsonify({"success": False, "error": str(ex)}), 500

@main.route('/<id>', methods=['GET'])
def get_editorial(id):
    try:
        editorial = EditorialModel.get_by_id(id)
        if editorial:
            return jsonify({"success": True, "message": "Editorial encontrada", "data": editorial}), 200
        return jsonify({"success": False, "message": "Editorial no encontrada"}), 404
    except Exception as ex:
        return jsonify({"success": False, "error": str(ex)}), 500

@main.route('/add', methods=['POST'])
def add_editorial():
    try:
        data = request.get_json()
        
        if 'nombre' not in data:
            return jsonify({
                "success": False,
                "error": "El campo 'nombre' es obligatorio"
            }), 400

        editorial = Editorial(
            id=str(uuid.uuid4()),
            nombre=data['nombre']
        )
        
        affected_rows = EditorialModel.add(editorial)
        if affected_rows == 1:
            return jsonify({
                "success": True,
                "message": "Editorial registrada",
                "id": editorial.id
            }), 201
            
        return jsonify({"success": False, "error": "No se pudo registrar"}), 400
    except Exception as ex:
        return jsonify({"success": False, "error": str(ex)}), 500

@main.route('/update/<id>', methods=['PUT'])
def update_editorial(id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "Datos requeridos"}), 400

        editorial = Editorial(
            id=id,
            nombre=data.get('nombre')
        )
        
        affected_rows = EditorialModel.update(editorial)
        if affected_rows == 1:
            return jsonify({"success": True, "message": "Editorial actualizada"}), 200
        return jsonify({"success": False, "error": "No se actualizó"}), 400
    except Exception as ex:
        return jsonify({"success": False, "error": str(ex)}), 500

@main.route('/delete/<id>', methods=['DELETE'])
def delete_editorial(id):
    try:
        affected_rows = EditorialModel.delete(id)
        if affected_rows == 1:
            return jsonify({"success": True, "message": "Editorial eliminada"}), 200
        return jsonify({"success": False, "error": "No se eliminó"}), 400
    except Exception as ex:
        return jsonify({"success": False, "error": str(ex)}), 500