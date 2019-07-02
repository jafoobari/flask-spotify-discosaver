# Quickstart

Runs on Python 3.6.0 in production.

To set up a new local environment:
```
$ git clone https://gitlab.com/jallen92/flask-spotify.git
$ python3 -m venv venv
$ source venv/Scripts/activate
$ pip install -r requirements.txt
```

To activate virtual environment on production machine:
```
$ workon flask-SP-virtualenv
```

To ensure you have the latest changes:
```
$ git pull origin master
```

To run web app locally:
```
$ export FLASK_APP=spotify_dw.py
$ export FLASK_CONFIG=dev
$ flask run
```

If you update database models be sure to migrate and then upgrade:
```
$ export FLASK_APP=spotify_dw.py
$ flask db migrate -m "playlists and songs tables"
$ flask db upgrade
```
(Also, don't forget to import any new database models to spotify_dw.py for the shell and any other appropriate files that use the models.)

To get a specific remote branch for local development:
```
$ git pull origin <rbranch>:<lbranch>
$ git checkout <lbranch>
```

## Merging

To merge a branch with master:
```
$ git checkout <branch>
$ git merge master #to keep master clean while resolving any conflicts
$ git checkout master
$ git merge <branch> #should be a clean merge
```

Tag branches after merging and before deleting:
```
$ git checkout <branch>
$ git tag -a <version> -m "<version description>"
$ git push origin <version> #push the tag to the remote repo
```

Finally, delete the branch:
```
$ git checkout master
$ git branch -d <branch>
$ git push origin :<branch> #delete the branch from the remote repo
```

### Using the Shell

The function that creates the shell is in spotify_dw.py. Be sure you are importing everything you want there.

Run the shell with: `flask shell`

### Misc

Helpful guides:
* https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
* https://flask-sqlalchemy.palletsprojects.com/en/2.x/
