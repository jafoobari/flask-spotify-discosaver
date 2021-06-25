from datetime import datetime
from dw_saver import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    weekly_scheduled = db.Column(db.Boolean, default=False)
    monthly_scheduled = db.Column(db.Boolean, default=False)
    access_token = db.Column(db.String(256))
    refresh_token = db.Column(db.String(256))
    token_expires_at = db.Column(db.Integer)
    token_expires_in = db.Column(db.Integer)
    token_scope = db.Column(db.String(256))
    token_type = db.Column(db.String(32))
    dw_playlist_id = db.Column(db.String(256))

    def __repr__(self):
        return '<User {}>'.format(self.username)
