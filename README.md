# Quickstart

Runs on Python 3.6.0 in production.

### To set up a new local environment:

If using macOS, probably is a good idea to ensure you're using python 3.6.0 since that's what the project expects. We can use `pyenv` to help with that.

```
$ brew install pyenv
$ git clone https://gitlab.com/jallen92/flask-spotify.git
$ cd flask-spotify
$ pyenv install 3.6.0
$ pyenv local 3.6.0
$ pyenv exec python3 -V
$ pyenv exec python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

If using Windows (haven't checked if any uses with using python versions greater than 3.6.0):

```
$ python3 -m venv venv
$ source venv/Scripts/activate
$ pip install -r requirements.txt
```

To activate virtual environment on production machine (pythonanywhere):
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

If you need to update database models from the newest migration:
```
$ flask db upgrade
```

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
