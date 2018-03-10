from datetime import date, timedelta

from app import app, db
from app.models import User

import spotipy

today = date.today()
last_monday = today - timedelta(days=today.weekday())

client_id = app.config['CLIENT_ID']
client_secret = app.config['CLIENT_SECRET']
redirect_uri = app.config['REDIRECT_URI']
scope = app.config['SCOPE']
oauth = spotipy.oauth2.SpotifyOAuth(client_id, client_secret,
                                    redirect_uri, scope = scope)

users = User.query.all()

def dict_index_by_key(lst, key, value):
    for i,d in enumerate(lst):
        if d[key] == value:
            return i
    return -1

def is_token_expired(expires_at, expires_in):
    now = int(datetime.timestamp(datetime.now()))
    return expires_at - now < (expires_in/60)

#TODO: store token_info in database and check if token is expired.
for user in users:
    if is_token_expired(user.token_expires_at, user.token_expires_in) == True:
        fresh_token_info = oauth.refresh_access_token(user.refresh_token)
        sp = spotipy.Spotify(auth=fresh_token_info['access_token'])
        user.access_token = fresh_token_info['access_token']
        user.token_expires_at = fresh_token_info['expires_at']
        user.token_expires_in = fresh_token_info['expires_in']
        db.session.commit()          
    else:
        sp = spotipy.Spotify(auth=user.access_token)                         
    username = user.username
    playlists = sp.current_user_playlists()['items']    
    dscvr_wkly_playlist = playlists[dict_index_by_key(playlists, 'name',
                                                      'Discover Weekly')]
                                                      
    dscvr_wkly_tracks = sp.user_playlist_tracks('spotify',
                                                dscvr_wkly_playlist['id'])
    
    track_ids = [d['track']['id'] for d in dscvr_wkly_tracks['items']]
    new_archived_playlist = sp.user_playlist_create(username, 
                                                    'DW-'+str(last_monday), 
                                                    public=False)
    sp.user_playlist_add_tracks(username,
                                new_archived_playlist['id'],
                                track_ids)
    dw_url = new_archived_playlist['external_urls']['spotify']
        
        
