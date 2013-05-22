from flask import Flask, request, Response
from models import db, Cover, MediaType, User, Module, MediaSource
from queries import get_media_types
from settings import DATABASE_URI
from functools import wraps
import json
import hashlib

application = Flask(__name__)
db.init_app(application)
db.app = application
application.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def check_auth(users):
    auth = request.authorization
    for user in users:
        if user[0] == auth.username and user[1] == hashlib.md5(auth.password).hexdigest():
            return True
    return False

def requires_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        users = db.session.query(User.email, User.password).filter(User.admin == True).all()
        if check_auth(users):
            return f(*args, **kwargs)
        else:
            return authenticate()
    return decorated

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        users = db.session.query(User.email, User.password).all()
        if check_auth(users):
            return f(*args, **kwargs)
        else:
            return authenticate()
    return decorated

### MEDIA TYPE ###
@application.route('/mediatypes/', methods=['GET'])
def mediatypes_get():
	pass

@application.route('/mediatype/', methods=['POST'])
def mediatype_post():
	pass

@application.route('/mediatype/<id>/', methods=['GET'])
def mediatype_get():
	pass

@application.route('/mediatype/<id>/', methods=['PUT'])
def mediatype_put():
	pass
###

### USER ###
@application.route('/users/', methods=['GET'])
@requires_admin
def users_get():
    return str(db.session.query(User.cover_id, User.name, User.email, User.password, User.admin).all())

@application.route('/user/', methods=['POST'])
def user_post():
	pass

@application.route('/user/<id>/', methods=['GET'])
def user_get():
	pass

@application.route('/me/', methods=['GET'])
def me_get():
	pass

@application.route('/me/', methods=['PUT'])
def me_put():
	pass
###

### MEDIA SOURCE ###
@application.route('/mediatype/<id>/', methods=['POST'])
def mediasource_post():
	pass

@application.route('/mediatype/<id>/<mediasource_id>/', methods=['GET'])
def mediasource_get():
	pass

@application.route('/mediatype/<id>/<mediasource_id>/', methods=['PUT'])
def mediasource_put():
	pass
###


if __name__ == '__main__':
    application.run(debug=True)

