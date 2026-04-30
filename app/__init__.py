# app/__init__.py
from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_restx import Api
from .config import Config
import os

db = SQLAlchemy()

api = Api(
    title='API Gestión de Casilleros',
    version='1.0',
    description='API REST para la gestión de asignación de casilleros y bitácora',
    doc='/docs'
)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # === LA LÍNEA MÁGICA QUE EVITA EL ERROR 500 ===
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

    db.init_app(app)
    CORS(app)
    api.init_app(app)

    # Crear carpeta uploads si no existe (aunque ya no la usemos para guardar, 
    # es buena práctica dejarla por si tienes el send_from_directory)
    if not os.path.exists(app.config.get('UPLOAD_FOLDER', 'uploads')):
        os.makedirs(app.config.get('UPLOAD_FOLDER', 'uploads'))

    # Importar rutas y modelos
    from .models import Assignment, Bitacora
    from .routes import bp as assignments_namespace
    from .bitacora import bitacora_namespace  # ← NUEVA IMPORTACIÓN
    from .horarios import horarios_namespace  # ← NUEVA IMPORTACIÓN

    # importar rutas y modelos de manto
    from app.manto.inventario import ns as inventario_ns
    from app.manto.prestamos import ns as prestamos_ns
    from app.manto.bitacora import ns as bitacora_ns
    from app.manto.sesiones import ns as sesiones_ns
    from app.manto.tarjetas import ns as tarjetas_ns
    from app.manto.tarjeta_material import ns as tarjeta_material_ns
    from app.manto.evidencias import ns as evidencias_ns


    # Registrar namespaces
    api.add_namespace(assignments_namespace, path='/assignments')
    api.add_namespace(bitacora_namespace, path='/bitacora')  # ← NUEVO ENDPOINT
    api.add_namespace(horarios_namespace, path='/horarios')  # ← NUEVO ENDPOINT

    # Registrar namespaces de manto
    api.add_namespace(inventario_ns)
    api.add_namespace(prestamos_ns)
    api.add_namespace(bitacora_ns)
    api.add_namespace(sesiones_ns)
    api.add_namespace(tarjetas_ns)
    api.add_namespace(tarjeta_material_ns)
    api.add_namespace(evidencias_ns)
    

    # Ruta para servir fotos
    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    with app.app_context():
        db.create_all()

    return app
