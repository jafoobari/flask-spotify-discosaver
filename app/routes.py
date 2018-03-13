from flask import render_template, redirect, request, session
from app import app, db, tools
from app.models import User
#TODO: Figure out how to clean up redundant imports


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
    #TODO: See if way to move most of below into tools.py
    token_info = tools.oauth.get_access_token(code)                         
    sp = tools.spotipy.Spotify(auth=token_info['access_token'])
    username = sp.current_user()['id']
    session['username'] = username
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
    if tools.is_token_expired(user) == True:
        tools.refresh_and_save_token(user)                                          
    dw_url = tools.save_discover_weekly(user.access_token)
    return render_template('playlist-saved.html', username=username,
                           dw_url=dw_url)

    
@app.route('/connect-spotify')
def auth():
    if not session.get('username'):
        return redirect(tools.oauth.get_authorize_url())
    else:
        return render_template('return_visitor.html', username=session.get('username'))
    
