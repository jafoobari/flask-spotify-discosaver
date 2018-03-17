from dw_saver import app, db
from dw_saver.models import User

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}