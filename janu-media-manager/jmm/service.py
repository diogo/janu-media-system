from flask import Flask, request
from models import db
from settings import DATABASE_URI
from responses import _401, _200
from functools import wraps
from token_manager import TokenManager
from media_manager import MediaManager
import json
import hashlib

tokenman = TokenManager()
mediaman = MediaManager()

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
                    kwargs['user_id'] = client['user']['id']
                    return f(*args, **kwargs)
        return _401
    return decorated

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.args.has_key('token'):
            client = tokenman.get_client(request.args['token'])
            if client:
                kwargs['user_id'] = client['user']['id']
                return f(*args, **kwargs)
        return _401
    return decorated

def check_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        kwargs['user_id'] = None
        if request.args.has_key('token'):
            client = tokenman.get_client(request.args['token'])
            if client:
                kwargs['user_id'] = client['user']['id']
        return f(*args, **kwargs)
    return decorated

def check_mediasources(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.args.has_key('mediasources'):
            mediasources = request.args['mediasources'].split(',')
            if mediasources:
                kwargs['mediasources'] = mediasources
                return f(*args, **kwargs)
        return _401
    return decorated

### TOKEN ###
@application.route('/get_token/', methods=['GET'])
def get_token():
    if request.authorization:
        email = request.authorization['username']
        password = hashlib.md5(request.authorization['password']).hexdigest()
        user = mediaman.get_user(email, password)
        if user:
            token = tokenman.get_token(user, request.user_agent, request.remote_addr)
            return json.dumps(token)
    return _401

@application.route('/expire_token/', methods=['GET'])
def expire_token():
    pass
######

### ARTIST ###
@application.route('/artist/', methods=['GET'])
@check_mediasources
@check_auth
def get_artists(*args, **kwargs):
    artists = mediaman.get_artists(kwargs['mediasources'], kwargs['user_id'])
    if artists:
        return json.dumps(artists)
    return _401

@application.route('/artist/<id>/playlist/', methods=['GET'])
@check_mediasources
@check_auth
def get_playlists_by_artist(**kwargs):
    playlists = mediaman.get_playlists_by_artist(kwargs['id'], kwargs['mediasources'], kwargs['user_id'])
    if playlists:
        return json.dumps(playlists)
    return _401

@application.route('/artist/<id>/media/', methods=['GET'])
@check_mediasources
@check_auth
def get_medias_by_artist(*args, **kwargs):
    medias = mediaman.get_medias_by_artist(kwargs['id'], kwargs['mediasources'], kwargs['user_id'])
    if medias:
        return json.dumps(medias)
    return _401
######

### PLAYLIST ###
@application.route('/playlist/<id>/media/', methods=['GET'])
@check_mediasources
@check_auth
def get_medias_by_playlist(**kwargs):
    medias = mediaman.get_medias_by_playlist(kwargs['id'], kwargs['mediasources'], kwargs['user_id'])
    if medias:
        return json.dumps(medias)
    return _401
######

### GENRE ###
@application.route('/genre/', methods=['GET'])
@check_mediasources
@check_auth
def get_genres(*args, **kwargs):
    genres = mediaman.get_genres(kwargs['mediasources'], kwargs['user_id'])
    if genres:
        return json.dumps(genres)
    return _401

@application.route('/genre/<id>/artist/', methods=['GET'])
@check_mediasources
@check_auth
def get_artists_by_genre(*args, **kwargs):
    artists = mediaman.get_artists_by_genre(kwargs['id'], kwargs['mediasources'], kwargs['user_id'])
    if artists:
        return json.dumps(artists)
    return _401
######

### MEDIA ###
@application.route('/media/<id>/', methods=['GET'])
@check_auth
def get_media(**kwargs):
    media = mediaman.get_media(kwargs['id'], kwargs['user_id'])
    if media:
        return json.dumps(media)
    return _401
######

### MEDIA TYPE ###
@application.route('/mediatype/', methods=['GET'])
@check_mediasources
@check_auth
def mediatypes_get(**kwargs):
    return json.dumps(mediaman.get_media_types(system_user=SYSTEM_USER))

@application.route('/mediatype/<id>/', methods=['GET'])
@check_mediasources
@check_auth
def mediatype_get(**kwargs):
	pass
######

### MEDIA SOURCE ###
@application.route('/mediasource/', methods=['GET'])
@requires_admin
def get_mediasources(**kwargs):
    return json.dumps(mediaman.get_mediasources(kwargs['user_id']))

@application.route('/mediasource/<id>/', methods=['GET'])
@requires_admin
def get_mediasource(**kwargs):
    pass

@application.route('/mediasource/', methods=['POST'])
@requires_admin
def add_mediasource(**kwargs):
    data = request.form
    data = {key: value for key, value in data.items()}
    data['user_id'] = kwargs['user_id']
    if mediaman.add_mediasource(data):
        return _200
    else:
        return _401

@application.route('/mediasource/<id>/', methods=['PUT'])
@requires_admin
def edit_mediasource(**kwargs):
    pass

@application.route('/mediasource/<id>/', methods=['DELETE'])
@requires_admin
def remove_mediasource(**kwargs):
    try:
        mediaman.remove_mediasource(kwargs['id'])
        return _200
    except Exception, e:
        print e
        return _401
######

### USER ###
@application.route('/user/', methods=['GET'])
@requires_admin
def get_users(**kwargs):
    return json.dumps(mediaman.get_users())

@application.route('/user/<id>/', methods=['GET'])
@requires_admin
def get_user():
	pass

@application.route('/user/', methods=['POST'])
def add_user():
    pass

@application.route('/me/', methods=['GET'])
@requires_auth
def get_me():
	pass

@application.route('/me/', methods=['PUT'])
@requires_auth
def edit_me():
	pass
######


if __name__ == '__main__':
    application.run(debug=True)

