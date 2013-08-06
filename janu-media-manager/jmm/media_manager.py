from models import db, Cover, MediaType, User, Module, MediaSource, ContentType, Playlist
from models import Media, MediaArtists, MediaGenres, MediaPlaylists, Artist, Genre
from settings import SYSTEM_USER_ID
from sqlalchemy import or_
import mediasources.mediafire
import content_types.audio_mpeg

def _as_dict(list_):
    if list_:
        new_list = []
        for item in list_:
            new_list.append(item._asdict())
        return new_list
    return None

def _get_models_by_user(query, user_id):
	return query.filter(or_(User.id == user_id,
                            User.id == SYSTEM_USER_ID)).distinct().all()

def _get_query_by_artists(query):
	return query.filter(MediaArtists.artist_id == Artist.id,
						MediaArtists.media_id == Media.id,
						Media.source_id == MediaSource.id)

def get_artists(user_id=None):
 	artists = db.session.query(Artist.id, Artist.name, Cover.url.label('cover_url'))
 	artists = artists.join(Artist.cover)
 	artists = _get_query_by_artists(artists)
 	artists = _get_models_by_user(artists, user_id)
 	return _as_dict(artists)

def get_collections_by_artist(artist_id, user_id=None):
	collections = db.session.query(Playlist.id, Playlist.name, Cover.url.label('cover_url'), Artist.id.label('artist_id'))
	collections = collections.join(Playlist.cover)
	collections = collections.filter(Playlist.collection == True,
									 MediaPlaylists.playlist_id == Playlist.id,
									 MediaPlaylists.media_id == Media.id)
	collections = _get_query_by_artists(collections)
	collections = collections.filter(Artist.id == artist_id)
	collections = _get_models_by_user(collections, user_id)
	return _as_dict(collections)

def get_user(user_id, user_password=None):
    query = db.session.query(User.id, User.name, User.email, User.admin,
                             User.description, Cover.url.label('cover_url')).join(Cover)
    if user_password:
        user = query.filter(User.email == user_id, User.password == user_password).first()
    elif isinstance(user_id, int):
        user = query.filter(User.id == user_id).first()
    if user:
        return user._asdict()
    else:
        return None

def get_users():
    users = db.session.query(User.id, User.name, User.email, User.admin,
                             Cover.url.label('cover_url')).join(Cover).all()
    return _as_dict(users)

def get_media_sources(user_id=None):
    media_sources = db.session.query(MediaSource.id, MediaSource.name,
                                           Cover.url.label('cover_url'),
                                           Module.name.label('module_name'))
    media_sources = media_sources.join(MediaSource.cover)\
                                 .join(MediaSource.module)\
                                 .join(MediaSource.user)
    media_sources = _get_models_by_user(media_sources, user_id)
    return _as_dict(media_sources)


def add_mediasource(data):
    mediasource = MediaSource(name=data['name'], user_id=data['user_id'], module_id=data['module_id'])
    db.session.add(mediasource)
    db.session.commit()
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
    return True
