from datetime import date, timedelta
import spotipy


def dict_index_by_key(lst, key, value):
    for i,d in enumerate(lst):
        if d[key] == value:
            return i
    return -1


def save(access_token):
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