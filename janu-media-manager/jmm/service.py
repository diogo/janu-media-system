from flask import Flask, request
from models import db, Cover, MediaType, User, Module, MediaSource
from queries import DoQuery
from settings import DATABASE_URI, SYSTEM_USER
from responses import _401, _200
from functools import wraps
from token_manager import TokenManager
import json
import hashlib

tokenman = TokenManager()
doquery = DoQuery(db.session)

application = Flask(__name__)

db.init_app(application)
db.app = application
application.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

def requires_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.args.has_key('token'):
            client = tokenman.get_client(request.args['token'])
            if client:
                if client['user']['admin']:
                    return f(*args, **kwargs)
        return _401
    return decorated

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.args.has_key('token'):
            client = tokenman.get_client(request.args['token'])
            if client:
                return f(*args, **kwargs)
        return _401
    return decorated

### TOKEN ###
@application.route('/get_token/', methods=['GET'])
def get_token():
    if request.authorization:
        email = request.authorization['username']
        password = hashlib.md5(request.authorization['password']).hexdigest()
        user = doquery.get_user(email, password)
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
    return json.dumps(doquery.get_media_types(system_user=SYSTEM_USER))

@application.route('/mediatype/<id>/', methods=['GET'])
def mediatype_get():
	pass

@application.route('/mediatype/', methods=['POST'])
@requires_admin
def mediatype_post():
    data = request.form
    db.session.add(MediaType(name=data['name']))
    db.session.commit()
    return _200

@application.route('/mediatype/<id>/', methods=['PUT'])
def mediatype_put():
	pass
######

### MEDIA SOURCE ###
@application.route('/mediasources/', methods=['GET'])
def mediasources_get():
    return json.dumps(doquery.get_media_sources(system_user=SYSTEM_USER))

@application.route('/mediasource/<id>/', methods=['GET'])
@requires_admin
def mediasource_get():
    pass

@application.route('/mediasource/', methods=['POST'])
@requires_admin
def mediasource_post(id):
    data = request.form
    user = tokenman.clients[request.args['token']]['user']
    db.session.add(MediaSource(type_id=data['type_id'], name=data['name'],
                               user_id=user['id'], module_id=data['module_id']))
    db.session.commit()
    return _200

@application.route('/mediasource/<id>/', methods=['PUT'])
def mediasource_put():
    pass
######

### USER ###
@application.route('/users/', methods=['GET'])
@requires_admin
def users_get():
    return json.dumps(doquery.get_users())

@application.route('/user/<id>/', methods=['GET'])
@requires_admin
def user_get():
	pass

@application.route('/user/', methods=['POST'])
def user_post():
    pass

@application.route('/me/', methods=['GET'])
def me_get():
	pass

@application.route('/me/', methods=['PUT'])
def me_put():
	pass
######


if __name__ == '__main__':
    application.run(debug=True)

