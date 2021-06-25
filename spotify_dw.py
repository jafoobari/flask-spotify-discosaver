from dw_saver import app, db
from dw_saver.models import User
import dw_saver.tools as Tools

@app.shell_context_processor
def make_shell_context():
    #If you have db migrate problems comment out the below line, migrate, upgrade, then uncomment...then research real fix.
    my_user = User.query.filter_by(username='jabsybobabsy').first()
    return {'db': db, 'User': User, 'Tools': Tools, 'my_user': my_user}
