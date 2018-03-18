from os import getenv
from datetime import date

from dw_saver.tools import str_to_bool, save_all_users_dw


run_now = str_to_bool(getenv('RUN_JOB_NOW', False))

today = date.today()
today_weekday = today.weekday()    
weekdays_to_run = [0]
                        
if run_now:
    save_all_users_dw()
elif (today_weekday in weekdays_to_run):
    save_all_users_dw()