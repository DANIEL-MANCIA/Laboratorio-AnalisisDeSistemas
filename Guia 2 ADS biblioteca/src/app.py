import logging
from flask import Flask, jsonify
from flask_cors import CORS
from config.config import app_config

from apis.auditorias.routes import Auditoria
from apis.autores.routes import Autor
from apis.categorias.routes import Categoria
from apis.editoriales.routes import Editorial
from apis.inventario.routes import Inventario
from apis.libros.routes import Libro
from apis.proveedores.routes import Proveedor
from apis.ubicaciones.routes import Ubicacion

app = Flask(__name__)

CORS(app)

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Manejo de errores
@app.errorhandler(400)
def bad_request_error(error):
    app.logger.warning(f"Bad Request: {str(error)}")
    return jsonify({
        "success": False,
        "error": "bad_request",
        "message": "Solicitud incorrecta. Verifique los datos enviados."
    }), 400

@app.errorhandler(404)
def not_found_error(error):
    app.logger.warning(f"Not Found: {str(error)}")
    return jsonify({
        "success": False,
        "error": "not_found",
        "message": "Recurso no encontrado."
    }), 404

@app.errorhandler(405)
def method_not_allowed_error(error):
    app.logger.warning(f"Method Not Allowed: {str(error)}")
    return jsonify({
        "success": False,
        "error": "method_not_allowed",
        "message": "Método no permitido para esta ruta."
    }), 405

@app.errorhandler(500)
def internal_server_error(error):
    app.logger.error(f"Internal Server Error: {str(error)}")
    return jsonify({
        "success": False,
        "error": "internal_server_error",
        "message": "Ocurrió un error interno en el servidor."
    }), 500

@app.errorhandler(Exception)
def handle_unexpected_error(error):
    app.logger.error(f"Unexpected Error: {str(error)}")
    return jsonify({
        "success": False,
        "error": "unexpected_error",
        "message": "Ocurrió un error inesperado."
    }), 500

if __name__ == "__main__":
    app.config.from_object(app_config['development'])

    # Apartado para rutas
    app.register_blueprint(Auditoria.main, url_prefix='/api/auditorias')
    app.register_blueprint(Autor.main, url_prefix='/api/autores')
    app.register_blueprint(Categoria.main, url_prefix='/api/categorias')
    app.register_blueprint(Editorial.main, url_prefix='/api/editoriales')
    app.register_blueprint(Inventario.main, url_prefix='/api/inventarios')
    app.register_blueprint(Libro.main, url_prefix='/api/libros')
    app.register_blueprint(Proveedor.main, url_prefix='/api/proveedores')
    app.register_blueprint(Ubicacion.main, url_prefix='/api/ubicaciones')

    app.run(host='0.0.0.0', port=5000, debug=True)