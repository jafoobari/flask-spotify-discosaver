from datetime import date, timedelta

from app import db
from app.models import User

import spotipy

today = date.today()
last_monday = today - timedelta(days=today.weekday())

client_id = '8412e923acce48a8b99ada05b6ba1181'     
client_secret = 'fbcadd353812442aaf9bd8c2bf6f0801'
redirect_uri = 'http://localhost/8000'
scope = 'playlist-modify-private playlist-read-private'
oauth = spotipy.oauth2.SpotifyOAuth(client_id, client_secret,
                                    redirect_uri, scope = scope)

users = User.query.all()

def dict_index_by_key(lst, key, value):
    for i,d in enumerate(lst):
        if d[key] == value:
            return i
    return -1

#TODO: store token_info in database and check if token is expired.
for user in users:
    if user.refresh_token is not None:
        refresh_token = user.refresh_token
        username = user.username        
        fresh_token_info = oauth.refresh_access_token(refresh_token)
        token = fresh_token_info['access_token']
        #TODO:Put spotify logic in its own file -- should be modular
        sp = spotipy.Spotify(auth=token)
        playlists = sp.current_user_playlists()['items']    
        dscvr_wkly_playlist = playlists[dict_index_by_key(playlists,
                                                          'name',
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
        user.token = token
        db.session.commit()
        
        
