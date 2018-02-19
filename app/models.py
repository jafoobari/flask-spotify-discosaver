from app import db

#TODO: store token_info in database so can check for expiration.

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    token = db.Column(db.String(256))
    refresh_token = db.Column(db.String(256))

    def __repr__(self):
        return '<User {}>'.format(self.username)    