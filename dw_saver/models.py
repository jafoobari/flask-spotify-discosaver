from datetime import datetime
from dw_saver import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
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

class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    songs = db.relationship('Song', backref='playlist', lazy='dynamic')

    def __repr__(self):
        return '<Playlist {}>'.format(self.body)

#TODO: Think about how you want to do the relationship between songs and playlists.
#Because songs can show up in multiple playlists, it probably makes sense to not duplicateself.
#Perhaps this should be a many-to-many relationship b/w songs and playlists...

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title =
    artist =
    length =
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.id'))

    def __repr__(self):
        return '<Song {}>'.format(self.body)

song_playlist = db.Table('songs_playlists',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)
