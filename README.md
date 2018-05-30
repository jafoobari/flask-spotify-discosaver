# Quickstart

To set up a new local environment:
```
$ git clone https://gitlab.com/jallen92/flask-spotify.git
$ python3 -m venv flask_spotify
$ source flask_spotify/Scripts/activate
$ pip install -r requirements.txt
```

To ensure you have the latest changes:
```
$ git pull origin master
```

To run web app locally:
```
$ export FLASK_APP=spotify_dw.py
$ export FLASK_CONFIG=dev
$ flask db upgrade
$ flask run
```

To get a specific remote branch for local development:
```
$ git pull origin <rbranch>:<lbranch> 
$ git checkout <lbranch>
```