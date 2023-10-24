from os import getenv
from datetime import date

from dw_saver.tools import str_to_bool, save_all_users_dw, get_or_save_discover_weekly, is_token_expired, refresh_and_save_token
from dw_saver.models import User


run_now = str_to_bool(getenv('RUN_JOB_NOW', False))
my_weekly_now = str_to_bool(getenv('MY_WEEKLY_NOW', False))

today = date.today()
today_weekday = today.weekday()
weekdays_to_run = [0]

if my_weekly_now:
    print("Retrieving or saving Discover Weekly for jabsybobabsy only.")
    user = User.query.filter_by(username='jabsybobabsy').first()
    if is_token_expired(user) == True:
        refresh_and_save_token(user)
    print(get_or_save_discover_weekly(user))
elif run_now:
    save_all_users_dw()
elif (today_weekday in weekdays_to_run):
    save_all_users_dw()
else:
    print("Nothing ran.")
