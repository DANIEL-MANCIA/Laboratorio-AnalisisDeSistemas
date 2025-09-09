from flask import Blueprint, jsonify, request
from ..models.ProveedoresModels import ProveedorModel
from ..models.entities.Proveedores import Proveedor
import uuid

main = Blueprint("proveedores_blueprint", __name__)

@main.route('/', methods=['GET'])
def get_proveedores():
    try:
        proveedores = ProveedorModel.get_all()
        return jsonify({
            "success": True,
            "message": "Lista de proveedores",
            "data": proveedores,
            "count": len(proveedores)
        }), 200
    except Exception as ex:
        return jsonify({"success": False, "error": str(ex)}), 500

@main.route('/<id>', methods=['GET'])
def get_proveedor(id):
    try:
        proveedor = ProveedorModel.get_by_id(id)
        if proveedor:
            return jsonify({"success": True, "message": "Proveedor encontrado", "data": proveedor}), 200
        return jsonify({"success": False, "message": "Proveedor no encontrado"}), 404
    except Exception as ex:
        return jsonify({"success": False, "error": str(ex)}), 500

@main.route('/add', methods=['POST'])
def add_proveedor():
    try:
        data = request.get_json()
        
        if 'nombre' not in data:
            return jsonify({
                "success": False,
                "error": "El campo 'nombre' es obligatorio"
            }), 400

        proveedor = Proveedor(
            id=str(uuid.uuid4()),
            nombre=data['nombre'],
            contacto=data.get('contacto')
        )
        
        affected_rows = ProveedorModel.add(proveedor)
        if affected_rows == 1:
            return jsonify({
                "success": True,
                "message": "Proveedor registrado",
                "id": proveedor.id
            }), 201
            
        return jsonify({"success": False, "error": "No se pudo registrar"}), 400
    except Exception as ex:
        return jsonify({"success": False, "error": str(ex)}), 500

@main.route('/update/<id>', methods=['PUT'])
def update_proveedor(id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "Datos requeridos"}), 400

        proveedor = Proveedor(
            id=id,
            nombre=data.get('nombre'),
            contacto=data.get('contacto')
        )
        
        affected_rows = ProveedorModel.update(proveedor)
        if affected_rows == 1:
            return jsonify({"success": True, "message": "Proveedor actualizado"}), 200
        return jsonify({"success": False, "error": "No se actualizó"}), 400
    except Exception as ex:
        return jsonify({"success": False, "error": str(ex)}), 500

@main.route('/delete/<id>', methods=['DELETE'])
def delete_proveedor(id):
    try:
        affected_rows = ProveedorModel.delete(id)
        if affected_rows == 1:
            return jsonify({"success": True, "message": "Proveedor eliminado"}), 200
        return jsonify({"success": False, "error": "No se eliminó"}), 400
    except Exception as ex:
        return jsonify({"success": False, "error": str(ex)}), 500