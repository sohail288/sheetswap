from flask import Flask

from flask import (
    render_template,
    request,
    g,
    session,
    jsonify,
    Response
)

from flask.ext.bootstrap import Bootstrap
from flask.ext.script    import Manager

import os



app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '../templates'))

bootstrap = Bootstrap(app)

manager   = Manager(app)


@app.route('/')
def index():
    return render_template('main.html')

@app.route('/sheet-test')
def sheet_test():
    return render_template('items/index.html')

if __name__ == '__main__':
    manager.run()
