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

Can do a quick test run of running `jobs.py` from the terminal with the below commands. It will either grab (and print to terminal) the current week's *saved* Discover Weekly or create it if it doesn't exist (for jabsybobabsy).

```
$ export MY_WEEKLY_NOW=True
$ python jobs.py
```

Can set up scheduled task to run `jobs.py` from your local macOS machine using the `full_run_job_now` file (or test with `run_my_weekly_now`) and following the instructions [here](https://medium.com/analytics-vidhya/effortlessly-automate-your-python-scripts-cd295697dff6) (or as a backup, [here](https://martechwithme.com/schedule-python-scripts-windows-mac/)). Both require a top user level folder named `scheduled_tasks`

Note: make sure you're using python 3.6 for any/all commands. Should be automatic with the above `pyenv` and `venv` commands. But can verify with `python -V`. And can force usage of the local python version with `pyenv exec python3`.

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
