import os

# Carpeta base del módulo SIEM
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Usamos SQLite como base de datos local
DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'siem.db')

# Clave secreta para Flask (para sesiones, CSRF, etc.)
SECRET_KEY = 'cambia-esta-clave-en-produccion'

# Modo debug activado mientras desarrollas
DEBUG = True
