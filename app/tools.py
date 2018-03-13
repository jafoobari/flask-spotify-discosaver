from datetime import date, timedelta, datetime

import spotipy
import spotipy.util as util #Needed for spotipy.oauth2

from app import app, db

client_id = app.config['CLIENT_ID']
client_secret = app.config['CLIENT_SECRET']
redirect_uri = app.config['REDIRECT_URI']
scope = app.config['SCOPE']
oauth = spotipy.oauth2.SpotifyOAuth(client_id, client_secret,
                                    redirect_uri, scope = scope)

def dict_index_by_key(lst, key, value):
    for i,d in enumerate(lst):
        if d[key] == value:
            return i
    return -1

def is_token_expired(user):
    now = int(datetime.timestamp(datetime.now()))
    return user.token_expires_at - now < (user.token_expires_in/60)

def refresh_and_save_token(user):
    fresh_token_info = oauth.refresh_access_token(user.refresh_token)
    user.access_token = fresh_token_info['access_token']
    user.token_expires_at = fresh_token_info['expires_at']
    user.token_expires_in = fresh_token_info['expires_in']
    db.session.commit()
    db.session.refresh(user)

def save_discover_weekly(access_token):
    today = date.today()
    last_monday = today - timedelta(days=today.weekday())
    sp = spotipy.Spotify(auth=access_token) 
    username = sp.current_user()['id'] 
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
    return dw_url