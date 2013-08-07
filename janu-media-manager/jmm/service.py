from flask import Flask, request
from models import db, Cover, MediaType, User, Module, MediaSource, ContentType, Playlist
from models import Media, MediaArtists, MediaGenres, MediaPlaylists, Artist, Genre
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

@application.route('/artist/<id>/collections/', methods=['GET'])
@check_mediasources
@check_auth
def get_collections_by_artist(**kwargs):
    collections = mediaman.get_collections_by_artist(kwargs['id'], kwargs['mediasources'])
    if collections:
        return json.dumps(collections)
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

@application.route('/mediatype/', methods=['POST'])
@requires_auth
def mediatype_post(**kwargs):
    data = request.form
    db.session.add(MediaType(name=data['name']))
    db.session.commit()
    return _200

@application.route('/mediatype/<id>/', methods=['PUT'])
@requires_auth
def mediatype_put(**kwargs):
	pass
######

### MEDIA SOURCE ###
@application.route('/mediasource/', methods=['GET'])
@requires_auth
def mediasource_get_all(**kwargs):
    return json.dumps(mediaman.get_media_sources(kwargs['user_id']))

@application.route('/mediasource/<id>/', methods=['GET'])
@requires_auth
def mediasource_get(**kwargs):
    pass

@application.route('/mediasource/', methods=['POST'])
@requires_auth
def mediasource_post(**kwargs):
    data = request.form
    data = {key: value for key, value in data.items()}
    data['user_id'] = kwargs['user_id']
    if mediaman.add_mediasource(data):
        return _200
    else:
        return _401

@application.route('/mediasource/<id>/', methods=['PUT'])
@requires_auth
def mediasource_put(**kwargs):
    pass

@application.route('/mediasource/<id>/', methods=['DELETE'])
@requires_auth
def mediasource_delete(**kwargs):
    pass
######

### USER ###
@application.route('/user/', methods=['GET'])
@requires_auth
def users_get(**kwargs):
    return json.dumps(mediaman.get_users())

@application.route('/user/<id>/', methods=['GET'])
@requires_auth
def user_get():
	pass

@application.route('/user/', methods=['POST'])
def user_post():
    pass

@application.route('/me/', methods=['GET'])
@requires_auth
def me_get():
	pass

@application.route('/me/', methods=['PUT'])
@requires_auth
def me_put():
	pass
######


if __name__ == '__main__':
    application.run(debug=True)

