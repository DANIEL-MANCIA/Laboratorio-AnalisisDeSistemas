from decouple import config

# Define La clave secreta desde el archivo env o variable de entorno
class Config:
    SECRET_KEY = config('SECRET_KEY')

# Activa el modo debug para el entorno de desarrollo
class DevelopmentConfig(Config):
    DEBUG = True

# Diccionario para mapear nombres de entornos a sus configuraciones
app_config = {
    'development': DevelopmentConfig
}