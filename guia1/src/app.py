from flask import Flask
from flask_cors import CORS
from config.config import app_config

# Crear una instancia de la aplicación Flask
app = Flask(__name__)

# Habilitar CORS para todas las rutas y orígenes
# Esto permite que el frontend realice solicitudes a la API
CORS(app)

# Definir un manejador de errores para rutas no encontradas
def paginaNoEncontrada(error):
    return "<h1>Página no encontrada</h1>", 404

def errorServidor(error):
    return "<h1>Error interno del servidor</h1>", 500

@app.route('/')
def principal():
    return "<h1>Bienvenido a mi aplicacion con Flask - DANIEL MANCIA</h1>"

if __name__ == '__main__':
    # Cargamos la configuración para el entorno 'development'
    app.config.from_object(app_config['development'])

    # Registramos el manejador de errores 404
    app.register_error_handler(404, paginaNoEncontrada)
    app.register_error_handler(500, errorServidor)

    # Iniciamos el servidor de Flask, escuchando en el puerto 5000
    app.run(host='0.0.0.0', port=5000, debug=True)