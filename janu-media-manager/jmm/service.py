from flask import Flask, request
from models import db, Cover, MediaType, User, Module, MediaSource, ContentType, Playlist
from models import Media, MediaArtists, MediaGenres, MediaPlaylists, Artist, Genre
from settings import DATABASE_URI
from responses import _401, _200
from functools import wraps
from token_manager import TokenManager
import media_manager
import json
import hashlib

tokenman = TokenManager()

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

### TOKEN ###
@application.route('/get_token/', methods=['GET'])
def get_token():
    if request.authorization:
        email = request.authorization['username']
        password = hashlib.md5(request.authorization['password']).hexdigest()
        user = media_manager.get_user(email, password)
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
@requires_auth
def artist_get_all(**kwargs):
    artists = media_manager.get_artists(kwargs['user_id'])
    if artists:
        return json.dumps(artists)
    return _401

@application.route('/artist/<id>/', methods=['GET'])
def get_collections_by_artist(**kwargs):
    collections = media_manager.get_collections_by_artist(kwargs['id'])
    if collections:
        return json.dumps(collections)
    return _401
######

### MEDIA TYPE ###
@application.route('/mediatype/', methods=['GET'])
def mediatypes_get():
    return json.dumps(media_manager.get_media_types(system_user=SYSTEM_USER))

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
@application.route('/mediasource/', methods=['GET'])
@requires_auth
def mediasource_get_all(**kwargs):
    return json.dumps(media_manager.get_media_sources(kwargs['user_id']))

@application.route('/mediasource/<id>/', methods=['GET'])
@requires_admin
def mediasource_get(id):
    pass

@application.route('/mediasource/', methods=['POST'])
@requires_admin
def mediasource_post(**kwargs):
    data = request.form
    data = {key: value for key, value in data.items()}
    data['user_id'] = kwargs['user_id']
    if media_manager.add_mediasource(data):
        return _200
    else:
        return _401

@application.route('/mediasource/<id>/', methods=['PUT'])
def mediasource_put():
    pass

@application.route('/mediasource/<id>/', methods=['DELETE'])
def mediasource_delete():
    pass
######

### USER ###
@application.route('/user/', methods=['GET'])
@requires_admin
def users_get():
    return json.dumps(media_manager.get_users())

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

