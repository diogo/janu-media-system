from models import db, Cover, MediaType, User, Module, MediaSource, ContentType, Playlist
from models import Media, MediaArtists, MediaGenres, MediaPlaylists, Artist, Genre
from settings import SYSTEM_USER_ID, THREADS_MAX
from sqlalchemy import or_
import mediasources.mediafire
import content_types.audio_mpeg

class MediaManager(object):

    def _as_list_dict(self, list_):
        if list_:
            new_list = []
            for item in list_:
                item_dict = item._asdict()
                item_dict['date'] = item_dict['date'].strftime('%Y')
                new_list.append(item_dict)
            return new_list
        return None

    def _get_models_by_user(self, query, user_id):
        return query.filter(or_(User.id == user_id,
                                User.id == SYSTEM_USER_ID)).all()

    def _get_query_by_artists(self, query, artist_id=None):
        query = query.filter(MediaArtists.artist_id == Artist.id,
                            MediaArtists.media_id == Media.id)
        if artist_id:
            query = query.filter(Artist.id == artist_id)
        return query

    def _get_media_source_module(self, mediasource_id):
        mediasource = MediaSource.query.get(mediasource_id)
        module_class = mediasources.__dict__[mediasource.module.name].get_module_class()
        module = db.session.query(module_class).filter(module_class.media_source_id == mediasource_id).first()
        module.__init__()
        return module

    def _get_query_by_mediasources(self, query, mediasources_ids):
        list_ = []
        for ms in mediasources_ids:
            list_.append("Media.source_id == %s" % ms)
        mediasources = ', '.join(list_)
        return eval("query.filter(or_(%s))" % mediasources)

    def get_artists(self, mediasources_ids, user_id):
        artists = db.session.query(Artist.id, Artist.name, Cover.url.label('cover_url'))
        artists = artists.join(Artist.cover)
        artists = self._get_query_by_artists(artists)
        artists = self._get_query_by_mediasources(artists, mediasources_ids)
        artists = self._get_models_by_user(artists, user_id)
        return self._as_list_dict(artists)

    def get_collections_by_artist(self, artist_id, mediasources_ids, user_id):
        collections = db.session.query(Playlist.id, Playlist.name, Cover.url.label('cover_url'),
                                       Artist.id.label('artist_id'), Artist.name.label('artist_name'))
        collections = collections.join(Playlist.cover)
        collections = collections.filter(Playlist.collection == True,
                                         MediaPlaylists.playlist_id == Playlist.id,
                                         MediaPlaylists.media_id == Media.id)
        collections = self._get_query_by_mediasources(collections, mediasources_ids)
        collections = self._get_query_by_artists(collections, artist_id)
        collections = self._get_models_by_user(collections, user_id)
        return self._as_list_dict(collections)

    def get_medias_by_artist(self, artist_id, mediasources_ids, user_id):
        medias = db.session.query(Media.id, Media.name, Media.url, Media.date, Media.source_id,
                                  Artist.name.label('artist_name'), Artist.id.label('artist_id'))
        medias = self._get_query_by_mediasources(medias, mediasources_ids)
        medias = self._get_query_by_artists(medias, artist_id)
        medias = self._get_models_by_user(medias, user_id)
        return self._as_list_dict(medias)

    def get_medias_by_playlist(self, playlist_id, mediasources_ids, user_id):
        medias = db.session.query(Media.id, Media.name, Media.url, Media.date, Media.source_id,
                                  Playlist.name.label('playlist_name'), Playlist.id.label('playlist_id'),
                                  Artist.id.label('artist_id'), Artist.name.label('artist_name'))
        medias = medias.filter(Playlist.id == playlist_id,
                               MediaPlaylists.playlist_id == Playlist.id,
                               MediaPlaylists.media_id == Media.id,
                               MediaArtists.media_id == MediaPlaylists.media_id,
                               MediaArtists.artist_id == Artist.id)
        medias = self._get_query_by_mediasources(medias, mediasources_ids)
        medias = self._get_models_by_user(medias, user_id)
        return self._as_list_dict(medias)

    def get_media(self, media_id, user_id):
        media = db.session.query(Media.id, Media.name, Media.date, Media.url, Media.source_id).filter(Media.id == media_id)
        media = self._get_models_by_user(media, user_id)
        media = self._as_list_dict(media)[0]
        media['url'] = self._get_media_source_module(media['source_id']).get_media_url(media['url'])
        return media

    def get_user(self, user_id, user_password=None):
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

    def get_users(self):
        users = db.session.query(User.id, User.name, User.email, User.admin,
                                 Cover.url.label('cover_url')).join(Cover).all()
        return self._as_list_dict(users)

    def get_media_sources(self, user_id=None):
        media_sources = db.session.query(MediaSource.id, MediaSource.name,
                                               Cover.url.label('cover_url'),
                                               Module.name.label('module_name'))
        media_sources = media_sources.join(MediaSource.cover)\
                                     .join(MediaSource.module)\
                                     .join(MediaSource.user)
        media_sources = self._get_models_by_user(media_sources, user_id)
        return self._as_list_dict(media_sources)


    def add_mediasource(self, data):
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
