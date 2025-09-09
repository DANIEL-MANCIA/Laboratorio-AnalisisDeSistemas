from flask import Blueprint, jsonify, request
from ..models.UbicacionesModels import UbicacionModel
from ..models.entities.Ubicaciones import Ubicacion
import uuid

main = Blueprint("ubicaciones_blueprint", __name__)

@main.route('/', methods=['GET'])
def get_ubicaciones():
    try:
        ubicaciones = UbicacionModel.get_all()
        return jsonify({
            "success": True,
            "message": "Lista de ubicaciones",
            "data": ubicaciones,
            "count": len(ubicaciones)
        }), 200
    except Exception as ex:
        return jsonify({"success": False, "error": str(ex)}), 500

@main.route('/<id>', methods=['GET'])
def get_ubicacion(id):
    try:
        ubicacion = UbicacionModel.get_by_id(id)
        if ubicacion:
            return jsonify({"success": True, "message": "Ubicación encontrada", "data": ubicacion}), 200
        return jsonify({"success": False, "message": "Ubicación no encontrada"}), 404
    except Exception as ex:
        return jsonify({"success": False, "error": str(ex)}), 500

@main.route('/add', methods=['POST'])
def add_ubicacion():
    try:
        data = request.get_json()
        
        required_fields = ['sala', 'pasillo', 'estanteria']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                "success": False,
                "error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"
            }), 400

        ubicacion = Ubicacion(
            id=str(uuid.uuid4()),
            sala=data['sala'],
            pasillo=data['pasillo'],
            estanteria=data['estanteria'],
            seccion=data.get('seccion')
        )
        
        affected_rows = UbicacionModel.add(ubicacion)
        if affected_rows == 1:
            return jsonify({
                "success": True,
                "message": "Ubicación registrada",
                "id": ubicacion.id
            }), 201
            
        return jsonify({"success": False, "error": "No se pudo registrar"}), 400
    except Exception as ex:
        return jsonify({"success": False, "error": str(ex)}), 500

@main.route('/update/<id>', methods=['PUT'])
def update_ubicacion(id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "Datos requeridos"}), 400

        ubicacion = Ubicacion(
            id=id,
            sala=data.get('sala'),
            pasillo=data.get('pasillo'),
            estanteria=data.get('estanteria'),
            seccion=data.get('seccion')
        )
        
        affected_rows = UbicacionModel.update(ubicacion)
        if affected_rows == 1:
            return jsonify({"success": True, "message": "Ubicación actualizada"}), 200
        return jsonify({"success": False, "error": "No se actualizó"}), 400
    except Exception as ex:
        return jsonify({"success": False, "error": str(ex)}), 500

@main.route('/delete/<id>', methods=['DELETE'])
def delete_ubicacion(id):
    try:
        affected_rows = UbicacionModel.delete(id)
        if affected_rows == 1:
            return jsonify({"success": True, "message": "Ubicación eliminada"}), 200
        return jsonify({"success": False, "error": "No se eliminó"}), 400
    except Exception as ex:
        return jsonify({"success": False, "error": str(ex)}), 500