from flask import Flask, request
from models import db, Cover, MediaType, User, Module, MediaSource, ContentType, Playlist
from models import Media, MediaArtists, MediaGenres, MediaPlaylists, Artist, Genre
from queries import DoQuery
from settings import DATABASE_URI, SYSTEM_USER
from responses import _401, _200
from functools import wraps
from token_manager import TokenManager
import json
import hashlib
import mediasources.mediafire
import content_types.audio_mpeg

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
@application.route('/mediatype/', methods=['GET'])
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
@application.route('/mediasource/', methods=['GET'])
def mediasources_get():
    return json.dumps(doquery.get_media_sources(system_user=SYSTEM_USER))

@application.route('/mediasource/<id>/', methods=['GET'])
@requires_admin
def mediasource_get(id):
    pass

@application.route('/mediasource/', methods=['POST'])
@requires_admin
def mediasource_post():
    data = request.form
    user = tokenman.get_client(request.args['token'])['user']
    mediasource = MediaSource(name=data['name'], user_id=user['id'], module_id=data['module_id'])
    db.session.add(mediasource)
    db.session.commit()
    data = {key: value for key, value in data.items()}
    data['media_source_id'] = mediasource.id
    module_class = mediasources.__dict__[mediasource.module.name].get_module_class()
    module = module_class(data)
    db.session.add(module)
    db.session.commit()
    medias_model = []
    medias = module.get_all_medias()
    for media in medias:
        content_type = db.session.query(ContentType).filter(ContentType.name == media['content_type']).first()
        if content_type:
            content_type_id = content_type.id
            content_type = '_'.join(content_type.name.split('/'))
            content_type = content_types.__dict__[content_type]
            media_url = module.get_media_url(media['url'])
            media_dict = content_type.get_media_dict(media_url)
            if not media_dict:
                continue
            media_model = Media(name=media_dict['name'], content_type_id=content_type_id,
                                url=media['url'], source_id=mediasource.id)
            media_model.artist = media_dict['artist']
            media_model.genre = media_dict['genre']
            if media_dict.has_key('date'):
                media_model.date = media_dict['date']
            if media_dict.has_key('collection'):
                media_model.collection = media_dict['collection']
            if media_dict.has_key('collection_position'):
                media_model.coll_pos = media_dict['collection_position']
            db.session.add(media_model)
            medias_model.append(media_model)
    db.session.commit()

    for media in medias_model:
        artist_id = db.session.query(Artist.id).filter(Artist.name == media.artist).first()
        if artist_id:
            db.session.add(MediaArtists(artist_id=artist_id[0], media_id=media.id))
        else:
            artist = Artist(name=media.artist)
            db.session.add(artist)
            db.session.commit()
            db.session.add(MediaArtists(artist_id=artist.id, media_id=media.id))

        genre_id = db.session.query(Genre.id).filter(Genre.name == media.genre).first()
        if genre_id:
            db.session.add(MediaGenres(genre_id=genre_id[0], media_id=media.id))
        else:
            genre = Genre(name=media.genre)
            db.session.add(genre)
            db.session.commit()
            db.session.add(MediaGenres(genre_id=genre.id, media_id=media.id))

        if hasattr(media, 'collection'):
            playlist_id = db.session.query(Playlist.id).filter(Playlist.collection == True, Playlist.name == media.collection).first()
            if playlist_id:
                db.session.add(MediaPlaylists(playlist_id=playlist_id[0], media_id=media.id))
            else:
                playlist = Playlist(name=media.collection, collection=True)
                db.session.add(playlist)
                db.session.commit()
                db.session.add(MediaPlaylists(playlist_id=playlist.id, media_id=media.id))

    db.session.commit()
    for media in db.session.query(Media).all():
        print media.name, media.url, media.date, media.content_type.name, media.source.name
    for playlist in db.session.query(Playlist).all():
        print playlist.name
    for artist in db.session.query(Artist).all():
        print artist.name
    return _200

@application.route('/mediasource/<id>/', methods=['PUT'])
def mediasource_put():
    pass
######

### USER ###
@application.route('/user/', methods=['GET'])
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

