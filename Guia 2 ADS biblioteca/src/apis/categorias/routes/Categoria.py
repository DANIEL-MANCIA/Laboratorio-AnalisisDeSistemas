from flask import Blueprint, jsonify, request
from ..models.CategoriasModels import CategoriaModel
from ..models.entities.Categorias import Categoria
import uuid

main = Blueprint("categorias_blueprint", __name__)

@main.route('/', methods=['GET'])
def get_categorias():
    try:
        categorias = CategoriaModel.get_all()
        return jsonify({
            "success": True,
            "message": "Lista de categorías",
            "data": categorias,
            "count": len(categorias)
        }), 200
    except Exception as ex:
        return jsonify({"success": False, "error": str(ex)}), 500

@main.route('/<id>', methods=['GET'])
def get_categoria(id):
    try:
        categoria = CategoriaModel.get_by_id(id)
        if categoria:
            return jsonify({"success": True, "message": "Categoría encontrada", "data": categoria}), 200
        return jsonify({"success": False, "message": "Categoría no encontrada"}), 404
    except Exception as ex:
        return jsonify({"success": False, "error": str(ex)}), 500

@main.route('/add', methods=['POST'])
def add_categoria():
    try:
        data = request.get_json()
        
        if 'nombre' not in data:
            return jsonify({
                "success": False,
                "error": "El campo 'nombre' es obligatorio"
            }), 400

        categoria = Categoria(
            id=str(uuid.uuid4()),
            nombre=data['nombre']
        )
        
        affected_rows = CategoriaModel.add(categoria)
        if affected_rows == 1:
            return jsonify({
                "success": True,
                "message": "Categoría registrada",
                "id": categoria.id
            }), 201
            
        return jsonify({"success": False, "error": "No se pudo registrar"}), 400
    except Exception as ex:
        return jsonify({"success": False, "error": str(ex)}), 500

@main.route('/update/<id>', methods=['PUT'])
def update_categoria(id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "Datos requeridos"}), 400

        categoria = Categoria(
            id=id,
            nombre=data.get('nombre')
        )
        
        affected_rows = CategoriaModel.update(categoria)
        if affected_rows == 1:
            return jsonify({"success": True, "message": "Categoría actualizada"}), 200
        return jsonify({"success": False, "error": "No se actualizó"}), 400
    except Exception as ex:
        return jsonify({"success": False, "error": str(ex)}), 500

@main.route('/delete/<id>', methods=['DELETE'])
def delete_categoria(id):
    try:
        affected_rows = CategoriaModel.delete(id)
        if affected_rows == 1:
            return jsonify({"success": True, "message": "Categoría eliminada"}), 200
        return jsonify({"success": False, "error": "No se eliminó"}), 400
    except Exception as ex:
        return jsonify({"success": False, "error": str(ex)}), 500