'''
Core project file which imports the Flask app and sets
the Flask shell context for ease of use.
'''
from app import app, db
from app.models import User, Post
from app import cli

@app.shell_context_processor
def make_shell_context():
    '''
    Add the database, user, and post context to the shell session.
    When you run 'flask shell' in the command line then the following objects
    will become available in the session:
    db
    Post
    User
    '''
    return {'db': db, 'User': User, 'Post': Post}
