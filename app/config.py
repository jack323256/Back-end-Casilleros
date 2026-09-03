import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'mi_clave_secreta_super_segura_cambia_esto')

    # 🔒 Base de datos EXISTENTE (casilleros)
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'postgresql://neondb_owner:npg_TG6rSIHEAZd7@ep-proud-violet-anka3fy4.c-6.us-east-1.aws.neon.tech/neondb?sslmode=require'
    )

    # 🆕 Base de datos MANTO (NUEVA)
    SQLALCHEMY_BINDS = {
        'manto': os.environ.get(
            'MANTO_DATABASE_URL',
            'postgresql://neondb_owner:npg_TG6rSIHEAZd7@ep-proud-violet-anka3fy4.c-6.us-east-1.aws.neon.tech/neondb?sslmode=require'
        )
    }

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB máximo

    # Configuración de ruta absoluta y limpia
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.abspath(os.path.join(BASE_DIR, '..', 'uploads'))

    # Si existe como ARCHIVO, se borra para poder crear el DIRECTORIO
    if os.path.exists(UPLOAD_FOLDER) and os.path.isfile(UPLOAD_FOLDER):
        os.remove(UPLOAD_FOLDER)

    # Crear la carpeta si no existe
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
