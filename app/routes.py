from datetime import datetime

import spotipy
import spotipy.util as util #Needed for spotipy.oauth2 on L16


from flask import render_template, redirect, request, session
from app import app, db, save_discover_weekly
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
    token_info = oauth.get_access_token(code)   
    #TODO: Move literally all spotipy/spotify logic into own file/module                      
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
    user = User.query.filter_by(username=username).first()
    if is_token_expired(user) == True:
        refresh_and_save_token(user)                                          
    dw_url = save_discover_weekly.save(user.access_token)
    return render_template('playlist-saved.html', username=username,
                           dw_url=dw_url)

    
@app.route('/connect-spotify')
def auth():
    if not session.get('username'):
        return redirect(oauth.get_authorize_url())
    else:
        return render_template('return_visitor.html', username=session.get('username'))
    
