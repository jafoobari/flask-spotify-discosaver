from datetime import datetime
from dw_saver import db

#TODO: Move bulk of functions from tools.py and maybe routes.py to here
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
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
    playlists = db.relationship('Playlist', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

#Consider adding tags to playlists
class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    playlist_id = db.Column(db.String(64), index=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(120), index=True)
    songs = db.relationship('Song', backref='playlist', lazy='dynamic')

    def __repr__(self):
        return '<Playlist {}>'.format(self.body)

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    track_id = db.Column(db.String(64), index=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.id'))

    def __repr__(self):
        return '<Song {}>'.format(self.body)
