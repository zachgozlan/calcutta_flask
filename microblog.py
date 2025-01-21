from flask_app import app
from flask_app.models import Bid

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Bid': Bid}