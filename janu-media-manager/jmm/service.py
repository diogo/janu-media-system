from flask import Flask, request
from models import db, Cover, MediaType, User, Module, MediaSource
from settings import DATABASE_URI, SYSTEM_USER
from responses import _401, _200
from functools import wraps
from token_manager import TokenManager
import json
import queries
import hashlib

application = Flask(__name__)

db.init_app(application)
db.app = application
application.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

tokenman = TokenManager()

def requires_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.args.has_key('token'):
            token = request.args['token']
            if tokenman.clients.has_key(token):
                user = tokenman.clients[token]['user']
                if user['admin']:
                    return f(*args, **kwargs)
        return _401
    return decorated

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.args.has_key('token'):
            token = request.args['token']
            if tokenman.clients.has_key(token):
                return f(*args, **kwargs)
        return _401
    return decorated

### TOKEN ###
@application.route('/get_token/', methods=['GET'])
def get_token():
    if request.authorization:
        email = request.authorization['username']
        password = hashlib.md5(request.authorization['password']).hexdigest()
        user = queries.get_user(db.session, email, password)
        if user:
            token = tokenman.get_token(user, request.user_agent, request.remote_addr)
            return json.dumps(token)
    return _401

@application.route('/expire_token/', methods=['GET'])
def expire_token():
    pass
######

### MEDIA TYPE ###
@application.route('/mediatypes/', methods=['GET'])
def mediatypes_get():
    #user = tokenman.clients[request.args['token']]['user']
    return json.dumps(queries.get_media_types(db.session, system_user=SYSTEM_USER))

@application.route('/mediatype/', methods=['POST'])
@requires_admin
def mediatype_post():
    data = request.form
    db.session.add(MediaType(name=data['name']))
    db.session.commit()
    return _200

@application.route('/mediatype/<id>/', methods=['GET'])
def mediatype_get():
	pass

@application.route('/mediatype/<id>/', methods=['PUT'])
def mediatype_put():
	pass
######

### USER ###
@application.route('/users/', methods=['GET'])
@requires_admin
def users_get():
    return json.dumps(queries.get_users(db.session))

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
######

### MEDIA SOURCE ###
@application.route('/mediatype/<id>/', methods=['POST'])
@requires_auth
def mediasource_post(id):
    data = request.form
    user = tokenman.clients[request.args['token']]['user']
    db.session.add(MediaSource(type_id=id, name=data['name'],
                               user_id=user['id'], module_id=data['module_id']))
    db.session.commit()
    return _200

@application.route('/mediatype/<id>/<mediasource_id>/', methods=['GET'])
def mediasource_get():
	pass

@application.route('/mediatype/<id>/<mediasource_id>/', methods=['PUT'])
def mediasource_put():
	pass
######


if __name__ == '__main__':
    application.run(debug=True)

