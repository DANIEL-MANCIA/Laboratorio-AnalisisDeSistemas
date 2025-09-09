from flask import Blueprint, jsonify, request
from ..models.AutoresModels import AutorModel
from ..models.entities.Autores import Autor
import uuid

main = Blueprint("autores_blueprint", __name__)

@main.route('/', methods=['GET'])
def get_autores():
    try:
        autores = AutorModel.get_all()
        return jsonify({
            "success": True,
            "message": "Lista de autores",
            "data": autores,
            "count": len(autores)
        }), 200
    except Exception as ex:
        return jsonify({"success": False, "error": str(ex)}), 500

@main.route('/<id>', methods=['GET'])
def get_autor(id):
    try:
        autor = AutorModel.get_by_id(id)
        if autor:
            return jsonify({"success": True, "message": "Autor encontrado", "data": autor}), 200
        return jsonify({"success": False, "message": "Autor no encontrado"}), 404
    except Exception as ex:
        return jsonify({"success": False, "error": str(ex)}), 500

@main.route('/add', methods=['POST'])
def add_autor():
    try:
        data = request.get_json()
        
        required_fields = ['nombre', 'apellido']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                "success": False,
                "error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"
            }), 400

        autor = Autor(
            id=str(uuid.uuid4()),
            nombre=data['nombre'],
            apellido=data['apellido'],
            fecha_nacimiento=data.get('fecha_nacimiento'),
            nacionalidad=data.get('nacionalidad')
        )
        
        affected_rows = AutorModel.add(autor)
        if affected_rows == 1:
            return jsonify({
                "success": True,
                "message": "Autor registrado",
                "id": autor.id
            }), 201
            
        return jsonify({"success": False, "error": "No se pudo registrar"}), 400
    except Exception as ex:
        return jsonify({"success": False, "error": str(ex)}), 500

@main.route('/update/<id>', methods=['PUT'])
def update_autor(id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "Datos requeridos"}), 400

        autor = Autor(
            id=id,
            nombre=data.get('nombre'),
            apellido=data.get('apellido'),
            fecha_nacimiento=data.get('fecha_nacimiento'),
            nacionalidad=data.get('nacionalidad')
        )
        
        affected_rows = AutorModel.update(autor)
        if affected_rows == 1:
            return jsonify({"success": True, "message": "Autor actualizado"}), 200
        return jsonify({"success": False, "error": "No se actualizó"}), 400
    except Exception as ex:
        return jsonify({"success": False, "error": str(ex)}), 500

@main.route('/delete/<id>', methods=['DELETE'])
def delete_autor(id):
    try:
        affected_rows = AutorModel.delete(id)
        if affected_rows == 1:
            return jsonify({"success": True, "message": "Autor eliminado"}), 200
        return jsonify({"success": False, "error": "No se eliminó"}), 400
    except Exception as ex:
        return jsonify({"success": False, "error": str(ex)}), 500