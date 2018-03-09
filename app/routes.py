from datetime import date, datetime, timedelta
import os

import spotipy
import spotipy.util as util
from urllib.parse import urlparse


from flask import render_template, redirect, request, session
from app import app, db
from app.models import User


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

def is_token_expired(expires_at, expires_in):
    now = int(datetime.timestamp(datetime.now()))
    return expires_at - now < (expires_in/60)

@app.before_first_request
def setup_session():
    session.permanent = True
            
@app.route('/')
@app.route('/index')
def index():
    #TODO: Check for a cookie/local storage for user
    return render_template('index.html', title='Home')

@app.route('/success')
def callback():
    code = request.args.get('code')
    #TODO: Put all spotify logic in its own file -- should be modular    
    token_info = oauth.get_access_token(code)                         
    sp = spotipy.Spotify(auth=token_info['access_token'])
    username = sp.current_user()['id']
    session['username'] = username
    #TODO: Check for is user is in database before trying create and save.
    exists = db.session.query(
        db.session.query(User).filter_by(username=username).exists()
    ).scalar()
    if exists is False:
        user = User(username=username,
                    access_token=token_info['access_token'],
                    refresh_token=token_info['refresh_token'],
                    token_expires_at=token_info['expires_at'],
                    token_expires_in=token_info['expires_in'],
                    token_scope=token_info['scope'],
                    token_type=token_info['token_type'])
        db.session.add(user)
        db.session.commit()
    return render_template('success.html', username=username)
    

#TODO: Get username without passing it through URL. Perhaps via session.    
@app.route('/save-playlist/<username>')
def save_playlist(username):
    today = date.today()
    last_monday = today - timedelta(days=today.weekday())
    #TODO: Put below client info in a config file
    #TODO: Put all spotify logic in its own file -- should be modular
    
    user = User.query.filter_by(username=username).first()
    if is_token_expired(user.token_expires_at, user.token_expires_in) == True:
        fresh_token_info = oauth.refresh_access_token(user.refresh_token)
        sp = spotipy.Spotify(auth=fresh_token_info['access_token'])
        user.access_token = fresh_token_info['access_token']
        user.token_expires_at = fresh_token_info['expires_at']
        user.token_expires_in = fresh_token_info['expires_in']
        db.session.commit()          
    else:
        sp = spotipy.Spotify(auth=user.access_token)                         
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
    return render_template('playlist-saved.html', username=username,
                           dw_url=dw_url)

    
@app.route('/connect-spotify')
def auth():
    if not session.get('username'):
        return redirect(oauth.get_authorize_url())
    else:
        return render_template('return_visitor.html', username=session.get('username'))
    
