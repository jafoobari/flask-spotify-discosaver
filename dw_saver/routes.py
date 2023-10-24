from flask import render_template, redirect, request, session
from dw_saver import app, db, tools
from dw_saver.models import User
#TODO: Figure out how to clean up circular and redundant imports


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

    #TODO: See if way to move most of below into tools.py or rather models.py
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
                    token_type=token_info['token_type'],
                    weekly_scheduled=False,
                    monthly_scheduled=False)
        db.session.add(user)
        #Not sure if this will work, but we "need" user to exist in db in order to get dw_playlist_id
        dw_playlist = tools.find_playlist_by_name(user, 'Discover Weekly')
        user.dw_playlist_id = dw_playlist['id']
        db.session.commit()
    return render_template('success.html', username=username)


#TODO: Get username without passing it through URL. Perhaps via session.
@app.route('/save-playlist/<username>')
def save_playlist(username):
    user = User.query.filter_by(username=username).first()
    if tools.is_token_expired(user) == True:
        tools.refresh_and_save_token(user)
    new_saved_dw_playlist = tools.save_discover_weekly(user)
    dw_url = new_saved_dw_playlist['external_urls']['spotify']
    return render_template('playlist-saved.html', username=username,
                           dw_url=dw_url, dw_uri=new_saved_dw_playlist['uri'])

@app.route('/save-to-monthly-playlist/<username>')
def save_to_monthly_playlist(username):
    user = User.query.filter_by(username=username).first()
    if tools.is_token_expired(user) == True:
        tools.refresh_and_save_token(user)
    #TODO: Clean this up. Better var names, own template, etc.
    monthly_dw_playlist = tools.add_dw_tracks_to_monthly_dw(user)
    return render_template('playlist-saved.html', username=username,
                           dw_uri=monthly_dw_playlist['uri'])

#TODO: Check for existence of DW playlist on sign-up and save id for it in DB.
@app.route('/connect-spotify')
def auth():
    if not session.get('username'):
        return redirect(tools.oauth.get_authorize_url())
    else:
        username = session.get('username')
        user = User.query.filter_by(username=username).first()
        weekly_is_checked = user.weekly_scheduled
        monthly_is_checked = user.monthly_scheduled
        weekly_checkbox = 'checked' if weekly_is_checked else ""
        monthly_checkbox = 'checked' if monthly_is_checked else ""

        return render_template('settings.html', username=username,
                               weekly_checkbox=weekly_checkbox,
                               monthly_checkbox=monthly_checkbox)

@app.route('/settings', methods=['GET', 'POST'])
def save_settings():
    username = session.get('username')
    user = User.query.filter_by(username=username).first()
    if request.method == 'POST':
        weekly_is_checked = 'weekly' in request.form
        monthly_is_checked = 'monthly' in request.form
        if weekly_is_checked:
            user.weekly_scheduled = True
        else:
            user.weekly_scheduled = False
        if monthly_is_checked:
            user.monthly_scheduled = True
        else:
            user.monthly_scheduled = False
        db.session.commit()
    else:
        weekly_is_checked = user.weekly_scheduled
        monthly_is_checked = user.monthly_scheduled

    weekly_checkbox = 'checked' if weekly_is_checked else ""
    monthly_checkbox = 'checked' if monthly_is_checked else ""

    return render_template('settings.html', username=username,
                           weekly_checkbox=weekly_checkbox,
                           monthly_checkbox=monthly_checkbox)
