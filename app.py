from flask import Flask, request, jsonify
from database import init_db, db
from models import add_to_blacklist, check_blacklist
from utils.auth import require_token

app = Flask(__name__)
init_db(app)  # Crea la base de datos si no existe

@app.route('/blacklists', methods=['POST'])
@require_token
def add_email():
    data = request.get_json()
    email = data.get('email')
    app_uuid = data.get('app_uuid')
    reason = data.get('blocked_reason', '')
    ip_address = request.remote_addr

    if not email or not app_uuid:
        return jsonify({"error": "email y app_uuid son obligatorios"}), 400

    add_to_blacklist(email, app_uuid, reason, ip_address)
    return jsonify({
        "message": f"Email {email} agregado a la lista negra global.",
        "ip_address": ip_address
    }), 201


@app.route('/blacklists/<string:email>', methods=['GET'])
@require_token
def check_email(email):
    record = check_blacklist(email)
    if record:
        return jsonify({
            "blacklisted": True,
            "reason": record["blocked_reason"],
            "added_at": record["created_at"]
        }), 200
    else:
        return jsonify({"blacklisted": False}), 200


if __name__ == '__main__':
    app.run(debug=True)
