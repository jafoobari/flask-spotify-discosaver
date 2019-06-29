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
    
def find_playlist_by_name(user, name):
    sp = spotipy.Spotify(auth=user.access_token)
    playlists = sp.current_user_playlists()
    playlist_index = dict_index_by_key(playlists['items'], 'name', name)
    
    while not playlist_index and playlists['next']:
        playlists = sp.next(playlists)
        playlist_index = dict_index_by_key(playlists['items'], 'name', name)
        
    if playlist_index:
        return playlists['items'][playlist_index]
    else:
        return None
    
def dw_track_ids_from_playlist(user):
    sp = spotipy.Spotify(auth=user.access_token) 
    dw_playlist = find_playlist_by_name(user, 'Discover Weekly')
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
    #TODO: Don't grab all users; query just for scheduled users.    
    users = User.query.all()  
    for user in users:
        if (user.weekly_scheduled or user.monthly_scheduled):           
            if is_token_expired(user) == True:
                refresh_and_save_token(user)   
            if user.weekly_scheduled:               
                save_discover_weekly(user)
            if user.monthly_scheduled:
                add_dw_tracks_to_monthly_dw(user)
        
def create_monthly_dw(user, month, year):
    sp = spotipy.Spotify(auth=user.access_token)          
    monthly_dw_playlist = sp.user_playlist_create(user.username, 
                                                  f'DW-{month}-{year}', 
                                                  public=False)    
    return monthly_dw_playlist

def get_or_create_monthly_dw(user):
    today = date.today()
    month = today.strftime("%b")
    year = today.strftime("%Y")
    monthly_dw_playlist = (find_playlist_by_name(user, f'DW-{month}-{year}') or
                           create_monthly_dw(user, month, year))        
    return monthly_dw_playlist

def add_dw_tracks_to_monthly_dw(user):
    sp = spotipy.Spotify(auth=user.access_token)
    monthly_dw_playlist = get_or_create_monthly_dw(user)
    dw_track_ids = dw_track_ids_from_playlist(user)
    sp.user_playlist_add_tracks(user.username,
                                monthly_dw_playlist['id'],
                                dw_track_ids)
    return monthly_dw_playlist