from database import db  # Cambiar esta importación
from datetime import datetime

class Blacklist(db.Model):
    __tablename__ = 'blacklist'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    app_uuid = db.Column(db.String(36), nullable=False)
    blocked_reason = db.Column(db.String(255))
    ip_address = db.Column(db.String(45))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Método para agregar a la lista negra
    @classmethod
    def add_to_blacklist(cls, email, app_uuid, reason, ip_address):
        try:
            # Verificar si el email ya existe
            existing = cls.query.filter_by(email=email).first()
            if existing:
                raise Exception("Email ya existe en la lista negra")
            
            new_entry = cls(
                email=email,
                app_uuid=app_uuid,
                blocked_reason=reason,
                ip_address=ip_address
            )
            db.session.add(new_entry)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
    
    # Método para verificar si existe en lista negra
    @classmethod
    def check_blacklist(cls, email):
        record = cls.query.filter_by(email=email).first()
        if record:
            return {
                "blocked_reason": record.blocked_reason,
                "app_uuid": record.app_uuid,
                "ip_address": record.ip_address,
                "created_at": record.created_at
            }
        return None

# Funciones globales para mantener compatibilidad
def add_to_blacklist(email, app_uuid, reason, ip_address):
    return Blacklist.add_to_blacklist(email, app_uuid, reason, ip_address)

def check_blacklist(email):
    return Blacklist.check_blacklist(email)