from flask import Blueprint, jsonify, request
from ..models.LibrosModels import LibroModel
from ..models.entities.Libros import Libro
from datetime import datetime
import uuid

main = Blueprint("libros_blueprint", __name__)

@main.route('/', methods=['GET'])
def get_libros():
    try:
        libros = LibroModel.get_all()
        return jsonify({
            "success": True,
            "message": "Lista de libros",
            "data": libros,
            "count": len(libros)
        }), 200
    except Exception as ex:
        return jsonify({"success": False, "error": str(ex)}), 500

@main.route('/<id>', methods=['GET'])
def get_libro(id):
    try:
        libro = LibroModel.get_by_id(id)
        if libro:
            return jsonify({"success": True, "message": "Libro encontrado", "data": libro}), 200
        return jsonify({"success": False, "message": "Libro no encontrado"}), 404
    except Exception as ex:
        return jsonify({"success": False, "error": str(ex)}), 500

@main.route('/add', methods=['POST'])
def add_libro():
    try:
        data = request.get_json()
        
        required_fields = ['titulo', 'id_autor', 'id_editorial', 'id_categoria', 'id_ubicacion']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                "success": False,
                "error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"
            }), 400

        # Validar fecha de publicación si existe
        fecha_publicacion = None
        if 'fecha_publicacion' in data:
            try:
                fecha_publicacion = datetime.strptime(data['fecha_publicacion'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({
                    "success": False,
                    "error": "Formato de fecha inválido. Use YYYY-MM-DD"
                }), 400

        libro = Libro(
            id=str(uuid.uuid4()),
            titulo=data['titulo'],
            id_autor=data['id_autor'],
            id_editorial=data['id_editorial'],
            id_categoria=data['id_categoria'],
            id_ubicacion=data['id_ubicacion'],
            fecha_publicacion=fecha_publicacion,
            isbn=data.get('isbn')
        )
        
        affected_rows = LibroModel.add(libro)
        if affected_rows == 1:
            return jsonify({
                "success": True,
                "message": "Libro registrado",
                "id": libro.id
            }), 201
            
        return jsonify({"success": False, "error": "No se pudo registrar"}), 400
    except Exception as ex:
        return jsonify({"success": False, "error": str(ex)}), 500

@main.route('/update/<id>', methods=['PUT'])
def update_libro(id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "Datos requeridos"}), 400

        # Validar fecha de publicación si existe
        fecha_publicacion = None
        if 'fecha_publicacion' in data:
            try:
                fecha_publicacion = datetime.strptime(data['fecha_publicacion'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({
                    "success": False,
                    "error": "Formato de fecha inválido. Use YYYY-MM-DD"
                }), 400

        libro = Libro(
            id=id,
            titulo=data.get('titulo'),
            id_autor=data.get('id_autor'),
            id_editorial=data.get('id_editorial'),
            id_categoria=data.get('id_categoria'),
            id_ubicacion=data.get('id_ubicacion'),
            fecha_publicacion=fecha_publicacion,
            isbn=data.get('isbn')
        )
        
        affected_rows = LibroModel.update(libro)
        if affected_rows == 1:
            return jsonify({"success": True, "message": "Libro actualizado"}), 200
        return jsonify({"success": False, "error": "No se actualizó"}), 400
    except Exception as ex:
        return jsonify({"success": False, "error": str(ex)}), 500

@main.route('/delete/<id>', methods=['DELETE'])
def delete_libro(id):
    try:
        affected_rows = LibroModel.delete(id)
        if affected_rows == 1:
            return jsonify({"success": True, "message": "Libro eliminado"}), 200
        return jsonify({"success": False, "error": "No se eliminó"}), 400
    except Exception as ex:
        return jsonify({"success": False, "error": str(ex)}), 500