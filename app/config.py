import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'mi_clave_local_segura')
    #SECRET_KEY = 'mi_clave_secreta_super_segura_cambia_esto'

    # 🔒 Base de datos EXISTENTE (casilleros)
    #SQLALCHEMY_DATABASE_URI = (
    #    'mysql+pymysql://root:1234@localhost:3306/casilleros_db'
    #)

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

    # 🆕 Base de datos MANTO (NUEVA)
    #SQLALCHEMY_BINDS = {
    #    'manto': 'mysql+pymysql://root:1234@localhost:3306/manto'
    #}

    SQLALCHEMY_BINDS = {
        'manto': os.environ.get('DATABASE_URL_MANTO')
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
    
    # IMPORTANTE: Asegúrate de que la ruta exista al iniciar
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    # Añade esto para evitar errores de archivos pesados de cámara
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB máximo
