from flask import Flask, request
from flask_restful import Api, Resource
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from datetime import timedelta
import uuid
import re

# Importar configuraciones y módulos
from config import DATABASE_URL, BEARER_TOKEN
from database import db, init_db
from models import add_to_blacklist, check_blacklist, Blacklist

app = Flask(__name__)

# Configuración desde config.py
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = BEARER_TOKEN
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

# Inicializar extensiones
init_db(app)  # Usar la función de database.py
ma = Marshmallow(app)
jwt = JWTManager(app)
api = Api(app)

# Esquema Marshmallow
class BlacklistSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Blacklist
    
    email = ma.auto_field()
    app_uuid = ma.auto_field()
    blocked_reason = ma.auto_field()

blacklist_schema = BlacklistSchema()

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

# Recursos RESTful
class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        if not data:
            return {"error": "Se requiere JSON"}, 400
        
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return {"error": "Se requieren username y password"}, 400
        
        # VALIDACIÓN DE USUARIOS - MODIFICA ESTA PARTE SEGÚN TUS NECESIDADES
        users = {
            "admin": "admin123",
            "usuario1": "password1", 
            "app_user": "app123456"
        }
        
        # Verificar credenciales
        if username in users and users[username] == password:
            access_token = create_access_token(
                identity=username,
                additional_claims={"role": "admin"}  # Puedes agregar claims adicionales
            )
            return {
                "access_token": access_token,
                "token_type": "Bearer",
                "message": "Login exitoso",
                "user": username
            }, 200
        else:
            return {"error": "Credenciales inválidas"}, 401

class BlacklistResource(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        
        if not data:
            return {"error": "Se requiere JSON en el body"}, 400
        
        email = data.get('email')
        app_uuid = data.get('app_uuid')
        reason = data.get('blocked_reason', '')
        
        if not email:
            return {"error": "El campo 'email' es obligatorio"}, 400
        if not app_uuid:
            return {"error": "El campo 'app_uuid' es obligatorio"}, 400
        
        if not EMAIL_REGEX.match(email):
            return {"error": "Formato de email inválido"}, 400
        
        try:
            uuid.UUID(app_uuid)
        except ValueError:
            return {"error": "app_uuid no es un UUID válido"}, 400
        
        if reason and len(reason) > 255:
            return {"error": "blocked_reason no puede exceder 255 caracteres"}, 400
        
        ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
        if ',' in ip_address:
            ip_address = ip_address.split(',')[0].strip()
        
        try:
            # Usar la función del modelo
            add_to_blacklist(
                email=email, 
                app_uuid=app_uuid, 
                reason=reason, 
                ip_address=ip_address
            )
            
            return {
                "message": f"Email {email} agregado a la lista negra correctamente",
                "app_uuid": app_uuid,
                "blocked_reason": reason,
                "ip_address": ip_address
            }, 201
            
        except Exception as e:
            error_msg = str(e).lower()
            if "ya existe" in error_msg or "duplicate" in error_msg or "unique" in error_msg:
                return {"error": "El email ya existe en la lista negra"}, 409
            else:
                return {"error": f"Error interno del servidor: {str(e)}"}, 500

class BlacklistEmailResource(Resource):
    @jwt_required()
    def get(self, email):
        if not EMAIL_REGEX.match(email):
            return {"error": "Formato de email inválido"}, 400
        
        # Usar la función del modelo
        record = check_blacklist(email)
        if record:
            return {
                "blacklisted": True,
                "email": email,
                "reason": record["blocked_reason"],
                "app_uuid": record["app_uuid"],
                "ip_address": record["ip_address"],
                "added_at": record["created_at"].isoformat() if record["created_at"] else None
            }, 200
        else:
            return {
                "blacklisted": False,
                "email": email
            }, 200

# Registrar recursos
api.add_resource(LoginResource, '/auth/login')
api.add_resource(BlacklistResource, '/blacklists')
api.add_resource(BlacklistEmailResource, '/blacklists/<string:email>')

if __name__ == '__main__':
    app.run(debug=True, port=5600)