import os

class Config:
    # Nota: Dejaremos tu contraseña aquí solo por hoy para asegurar que arranque. 
    # Luego te enseñaré a ocultarla por seguridad.
    SECRET_KEY = 'mi_clave_secreta_super_segura_cambia_esto'

    # 🔒 Base de datos EXISTENTE (casilleros)
    # Fíjate que eliminé "-pooler" de la URL
    SQLALCHEMY_DATABASE_URI = 'postgresql://neondb_owner:npg_TG6rSIHEAZd7@ep-proud-violet-anka3fy4.c-6.us-east-1.aws.neon.tech/neondb?sslmode=require'

    # 🆕 Base de datos MANTO (NUEVA)
    SQLALCHEMY_BINDS = {
        'manto': 'postgresql://neondb_owner:npg_TG6rSIHEAZd7@ep-proud-violet-anka3fy4.c-6.us-east-1.aws.neon.tech/neondb?sslmode=require'
    }

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '..',
        'uploads'
    )

    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, '..', 'uploads')
    
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB máximo
