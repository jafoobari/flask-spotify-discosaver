# Quickstart

To set up a new local environment:
```
$ git clone https://gitlab.com/jallen92/flask-spotify.git
$ python3 -m venv venv
$ source venv/Scripts/activate
$ pip install -r requirements.txt
```

To ensure you have the latest changes:
```
$ git pull origin master
```

If you need to update database models:
```
$ flask db migrate -m "<message>"
$ flask db upgrade
```

To run web app locally:
```
$ export FLASK_APP=spotify_dw.py
$ export FLASK_CONFIG=dev
$ flask run
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

