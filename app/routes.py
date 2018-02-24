from datetime import date, datetime, timedelta
import os

import spotipy
import spotipy.util as util
from urllib.parse import urlparse


from flask import render_template, redirect, request
from app import app, db
from app.models import User


client_id = '8412e923acce48a8b99ada05b6ba1181'     
client_secret = 'fbcadd353812442aaf9bd8c2bf6f0801'
redirect_uri = 'http://localhost:5000/success'
scope = 'playlist-modify-private playlist-read-private'
oauth = spotipy.oauth2.SpotifyOAuth(client_id, client_secret,
                                    redirect_uri, scope = scope)


def dict_index_by_key(lst, key, value):
    for i,d in enumerate(lst):
        if d[key] == value:
            return i
    return -1

def is_token_expired(token_info):
    now = int(datetime.timestamp(datetime.now()))
    return token_info['expires_at'] - now < 60
            
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/success')
def callback():
    code = request.args.get('code')   
    #TODO: Put below client info in a config file
    #TODO: Put all spotify logic in its own file -- should be modular
    
    token_info = oauth.get_access_token(code)
    token = token_info['access_token']
    refresh_token = token_info['refresh_token']                          
    sp = spotipy.Spotify(auth=token)
    username = sp.current_user()['id']
    user = User(username=username, token=token, refresh_token=refresh_token)
    db.session.add(user)
    db.session.commit()
    return render_template('success.html', username=username)
    

    
@app.route('/save-playlist/<username>')
def save_playlist(username):
    today = date.today()
    last_monday = today - timedelta(days=today.weekday())
    #TODO: Put below client info in a config file
    #TODO: Put all spotify logic in its own file -- should be modular
    
    user = User.query.filter_by(username=username).first()
    fresh_token_info = oauth.refresh_access_token(user.refresh_token)
    token = fresh_token_info['access_token']                          
    sp = spotipy.Spotify(auth=token)
    
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
    #TODO: Update the user with new token_info...I guess?
    return render_template('playlist-saved.html', username=username,
                           dw_url = dw_url)

    
@app.route('/connect-spotify')
def auth():  
    return redirect(oauth.get_authorize_url())
