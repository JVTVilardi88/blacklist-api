from flask import request, jsonify
from config import BEARER_TOKEN

def require_token(f):
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Token requerido"}), 401
        token = auth_header.split(" ")[1]
        if token != BEARER_TOKEN:
            return jsonify({"error": "Token inválido"}), 403
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper