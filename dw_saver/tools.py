from datetime import date, timedelta, datetime

import spotipy
import spotipy.util as util #Needed for spotipy.oauth2

from dw_saver import app, db
from dw_saver.models import User

client_id = app.config['CLIENT_ID']
client_secret = app.config['CLIENT_SECRET']
redirect_uri = app.config['REDIRECT_URI']
scope = app.config['SCOPE']
oauth = spotipy.oauth2.SpotifyOAuth(client_id, client_secret,
                                    redirect_uri, scope = scope)

def str_to_bool(s):
    if s == 'True':
        return True
    else:
        return False


def dict_index_by_key(lst, key, value):
    for i,d in enumerate(lst):
        if d[key] == value:
            return i
    return None

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

def get_dw_playlist(user):
    sp = spotipy.Spotify(auth=user.access_token)  
    playlists = sp.current_user_playlists()['items']    
    dscvr_wkly_playlist = playlists[dict_index_by_key(playlists, 'name',
                                                      'Discover Weekly')]
    return dscvr_wkly_playlist

def dw_track_ids_from_playlist(user):
    sp = spotipy.Spotify(auth=user.access_token) 
    dw_playlist = get_dw_playlist(user)
    dw_tracks = sp.user_playlist_tracks('spotify',
                                        dw_playlist['id'])
    track_ids = [d['track']['id'] for d in dw_tracks['items']]
    return track_ids

def save_discover_weekly(user):
    today = date.today()
    last_monday = today - timedelta(days=today.weekday()) 
    sp = spotipy.Spotify(auth=user.access_token) 
    username = sp.current_user()['id']
    track_ids = dw_track_ids_from_playlist(user)   
    new_saved_dw_playlist = sp.user_playlist_create(username, 
                                                    'DW-'+str(last_monday), 
                                                    public=False)
    sp.user_playlist_add_tracks(username,
                                new_saved_dw_playlist['id'],
                                track_ids)
    dw_url = new_saved_dw_playlist['external_urls']['spotify']
    return new_saved_dw_playlist

def save_all_users_dw():    
    users = User.query.all()  
    for user in users:
        if is_token_expired(user) == True:
            refresh_and_save_token(user)          
        save_discover_weekly(user.access_token)

def check_for_monthly_dw(playlists, month):
    monthly_dw_index = dict_index_by_key(playlists,'name',
                                         f'DW-{month}')
    if monthly_dw_index == None:
        return None
    else:
        monthly_dw_playlist = playlists[monthly_dw_index]
        return monthly_dw_playlist
    
        
def create_monthly_dw(user, month):
    sp = spotipy.Spotify(auth=user.access_token)          
    monthly_dw_playlist = sp.user_playlist_create(user.username, 
                                                  f'DW-{month}', 
                                                  public=False)    
    return monthly_dw_playlist

def get_or_create_monthly_dw(user):
    sp = spotipy.Spotify(auth=user.access_token)
    today = date.today()
    current_month = today.strftime("%B")
    playlists = sp.current_user_playlists()['items'] 
    monthly_dw_playlist = check_for_monthly_dw(playlists, current_month)
    if monthly_dw_playlist == None:
        monthly_dw_playlist = create_monthly_dw(user, current_month)
        return monthly_dw_playlist
    else:
        return monthly_dw_playlist

def add_dw_tracks_to_monthly_dw(user):
    sp = spotipy.Spotify(auth=user.access_token)
    monthly_dw_playlist = get_or_create_monthly_dw(user)
    dw_track_ids = dw_track_ids_from_playlist(user)
    sp.user_playlist_add_tracks(user.username,
                                monthly_dw_playlist['id'],
                                dw_track_ids)
    return monthly_dw_playlist
    