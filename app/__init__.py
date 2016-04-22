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

BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR   = os.path.join(BASE_DIR, 'static')





