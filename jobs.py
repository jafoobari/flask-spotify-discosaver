import datetime

from dw_saver import tools
from dw_saver.models import User

today = datetime.date.today()
today_weekday = today.weekday()

weekdays_to_run = [0,4]

if (today_weekday in weekdays_to_run):
    users = User.query.all()
    
    for user in users:
        if tools.is_token_expired(user) == True:
            tools.refresh_and_save_token(user)          
        dw_url = tools.save_discover_weekly(user.access_token)
