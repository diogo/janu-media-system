from flask import Flask, request, Response
from models import db, Cover, MediaType, User, Module, MediaSource
from settings import DATABASE_URI
from functools import wraps
from flask_tokenauth import TokenAuth, _token_auth
import json
import queries
import hashlib

try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack

application = Flask(__name__)

db.init_app(application)
db.app = application
application.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

#auth = TokenAuth(application)
#application.config['TOKENAUTH_EXPIRE'] = 1

tokenauth = _token_auth(1)

def authenticate():
    return Response('', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_admin(f):
    @wraps(f)
    def decorated():
        args = request.args
        if args.has_key('token'):
            print tokenauth._clients
            if tokenauth._clients.has_key(args['token']):
                print 'OI'
                user = tokenauth._clients[args['token']]['user']
                if user['admin']:
                    return f()
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

### AUTH ###
@application.route('/login/', methods=['GET'])
def login():
    email = request.authorization['username']
    password = hashlib.md5(request.authorization['password']).hexdigest()
    user = queries.get_user(db.session, email, password)
    if user:
        token = tokenauth.get_token(email, password, request.user_agent, request.remote_addr)
        tokenauth._clients[token]['user'] = user
        return json.dumps({token: user})

@application.route('/logout/', methods=['GET'])
def logout():
    pass

@application.route('/sigin/', methods=['GET'])
def sigin():
    pass
######

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
######

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
######

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
######


if __name__ == '__main__':
    application.run(debug=True)

