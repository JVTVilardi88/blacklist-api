from datetime import datetime
from database import db

class Blacklist(db.Model):
    __tablename__ = 'blacklist'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    app_uuid = db.Column(db.String(36), nullable=False)
    blocked_reason = db.Column(db.String(255))
    ip_address = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

def add_to_blacklist(email, app_uuid, reason, ip_address):
    entry = Blacklist(email=email, app_uuid=app_uuid, blocked_reason=reason, ip_address=ip_address)
    db.session.add(entry)
    db.session.commit()

def check_blacklist(email):
    record = Blacklist.query.filter_by(email=email).first()
    if record:
        return {
            "blocked_reason": record.blocked_reason,
            "created_at": record.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
    return None
