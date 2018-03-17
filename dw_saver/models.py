from dw_saver import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    access_token = db.Column(db.String(256))
    refresh_token = db.Column(db.String(256))
    token_expires_at = db.Column(db.Integer)
    token_expires_in = db.Column(db.Integer)
    token_scope = db.Column(db.String(256))
    token_type = db.Column(db.String(32))

    def __repr__(self):
        return '<User {}>'.format(self.username)    