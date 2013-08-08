from models import db, Cover, MediaType, User, Module, MediaSource, ContentType, Playlist, FavoritePlaylist
from models import Media, MediaGenre, MediaPlaylist, Artist, Genre, FavoriteMedia
from settings import SYSTEM_USER_ID
from sqlalchemy import or_
import mediasources.mediafire
import content_types.audio_mpeg

class MediaManager(object):

    def _as_list_dict(self, list_):
        if list_:
            new_list = []
            for item in list_:
                item_dict = item._asdict()
                if item_dict.has_key('date'):
                    item_dict['date'] = item_dict['date'].strftime('%Y')
                new_list.append(item_dict)
            return new_list
        return None

    def _get_models_by_user(self, query, user_id):
        return query.filter(or_(User.id == user_id,
                                User.id == SYSTEM_USER_ID)).distinct().all()

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
        artists = artists.join(Artist.cover).filter(Media.artist_id == Artist.id)
        artists = self._get_query_by_mediasources(artists, mediasources_ids)
        artists = self._get_models_by_user(artists, user_id)
        return self._as_list_dict(artists)

    def get_playlists_by_artist(self, artist_id, mediasources_ids, user_id):
        collections = db.session.query(Playlist.id, Playlist.name, Cover.url.label('cover_url'), Playlist.collection,
                                       Artist.id.label('artist_id'), Artist.name.label('artist_name'))
        collections = collections.join(Playlist.cover)
        collections = collections.filter(MediaPlaylist.playlist_id == Playlist.id,
                                         MediaPlaylist.media_id == Media.id,
                                         Artist.id == Media.artist_id,
                                         Artist.id == artist_id)
        collections = self._get_query_by_mediasources(collections, mediasources_ids)
        collections = self._get_models_by_user(collections, user_id)
        return self._as_list_dict(collections)

    def get_playlists():
        pass

    def get_medias_by_artist(self, artist_id, mediasources_ids, user_id):
        medias = db.session.query(Media.id, Media.name,
                                  Cover.url.label('cover_url'))
        medias = medias.join(Media.cover, Media.artist).filter(Media.artist_id == artist_id)
        medias = self._get_query_by_mediasources(medias, mediasources_ids)
        medias = self._get_models_by_user(medias, user_id)
        return self._as_list_dict(medias)

    def get_medias_by_playlist(self, playlist_id, mediasources_ids, user_id):
        medias = db.session.query(Media.id, Media.name, Media.artist_id,
                                  Cover.url.label('cover_url'), Artist.name.label('artist_name'))
        medias = medias.join(Media.cover, Media.artist)
        medias = medias.filter(Playlist.id == playlist_id,
                               MediaPlaylist.playlist_id == Playlist.id,
                               MediaPlaylist.media_id == Media.id)
        medias = self._get_query_by_mediasources(medias, mediasources_ids)
        medias = self._get_models_by_user(medias, user_id)
        medias = self._as_list_dict(medias)
        if not medias:
            return None
        playlist = db.session.query(Playlist.id, Playlist.name, Cover.url.label('cover_url'))
        playlist = playlist.join(Playlist.cover).filter(Playlist.id == playlist_id).first()._asdict()
        playlist['medias'] = medias
        return playlist

    def get_media(self, media_id, user_id):
        media = db.session.query(Media.id, Media.name, Media.date, Media.url, Media.source_id).filter(Media.id == media_id)
        media = self._get_models_by_user(media, user_id)
        media = self._as_list_dict(media)[0]
        media['url'] = self._get_media_source_module(media['source_id']).get_media_url(media['url'])
        return media

    def get_genres(self, mediasources_ids, user_id):
        genres = db.session.query(Genre.id, Genre.name, Cover.url.label('cover_url'))
        genres = genres.join(Genre.cover)
        genres = self._get_query_by_mediasources(genres, mediasources_ids)
        genres = self._get_models_by_user(genres, user_id)
        return self._as_list_dict(genres)

    def get_artists_by_genre(self, genre_id, mediasources_ids, user_id):
        artists = db.session.query(Artist.id, Artist.name, Cover.url.label('cover_url'))
        artists = artists.join(Artist.cover)
        artists = artists.filter(Genre.id == genre_id,
                                 MediaGenre.genre_id == Genre.id, MediaGenre.media_id == Media.id,
                                 Artist.id == Media.artist_id)
        artists = self._get_query_by_mediasources(artists, mediasources_ids)
        artists = self._get_models_by_user(artists, user_id)
        artists = self._as_list_dict(artists)
        if not artists:
            return None
        genre = db.session.query(Genre.name, Genre.id, Cover.url.label('cover_url'))
        genre = genre.join(Genre.cover).filter(Genre.id == genre_id).first()._asdict()
        genre['artists'] = artists
        return genre

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

    def get_mediasources(self, user_id=None):
        media_sources = db.session.query(MediaSource.id, MediaSource.name,
                                         Cover.url.label('cover_url'),
                                         Module.name.label('module_name'))
        media_sources = media_sources.join(MediaSource.cover)\
                                     .join(MediaSource.module)\
                                     .join(MediaSource.user)
        media_sources = self._get_models_by_user(media_sources, user_id)
        return self._as_list_dict(media_sources)

    def remove_mediasource(self, mediasource_id):
        medias = Media.query.filter(Media.source_id == mediasource_id).all()
        for media in medias:
            MediaPlaylist.query.filter(MediaPlaylist.media_id == media.id).delete()
            MediaGenre.query.filter(MediaGenre.media_id == media.id).delete()
            FavoriteMedia.query.filter(FavoriteMedia.media_id == media.id).delete()
            if media.cover_id != 1:
                Cover.query.filter(Cover.id == media.cover_id).delete()
            db.session.delete(media)
        module = self._get_media_source_module(mediasource_id)
        db.session.delete(module)
        mediasource = MediaSource.query.get(mediasource_id)
        db.session.delete(mediasource)

        playlists = db.session.query(Playlist).all()
        for playlist in playlists:
            if not MediaPlaylist.query.filter(MediaPlaylist.playlist_id == playlist.id).all():
                FavoritePlaylist.query.filter(FavoritePlaylist.playlist_id == playlist.id).delete()
                if playlist.cover_id != 1:
                    Cover.query.filter(Cover.id == playlist.cover_id).delete()
                db.session.delete(playlist)

        genres = db.session.query(Genre).all()
        for genre in genres:
            if not MediaGenre.query.filter(MediaGenre.genre_id == genre.id).all():
                if genre.cover_id != 1:
                    Cover.query.filter(Cover.id == genre.cover_id).delete()
                db.session.delete(genre)
        
        db.session.commit()

        artists = db.session.query(Artist).all()
        for artist in artists:
            if not Media.query.filter(Media.artist_id == artist.id).all():
                if artist.cover_id != 1:
                    Cover.query.filter(Cover.id == artist.cover_id).delete()
                db.session.delete(artist)

        db.session.commit()

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
                artist = Artist.query.filter(Artist.name == media_dict['artist']).first()
                if not artist:
                    artist = Artist(name=media_dict['artist'])
                db.session.add(artist)
                media_model = Media(name=media_dict['name'], content_type_id=content_type_id,
                                    url=media['url'], source_id=mediasource.id, artist=artist)
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
            for genre in media.genre:
                genre_id = db.session.query(Genre.id).filter(Genre.name == genre).first()
                if genre_id:
                    db.session.add(MediaGenre(genre_id=genre_id[0], media_id=media.id))
                else:
                    genre_ = Genre(name=genre)
                    db.session.add(genre_)
                    db.session.commit()
                    db.session.add(MediaGenre(genre_id=genre_.id, media_id=media.id))

            if hasattr(media, 'collection'):
                playlist_id = db.session.query(Playlist.id).filter(Playlist.collection == True, Playlist.name == media.collection).first()
                if playlist_id:
                    db.session.add(MediaPlaylist(playlist_id=playlist_id[0], media_id=media.id))
                else:
                    playlist = Playlist(name=media.collection, collection=True)
                    db.session.add(playlist)
                    db.session.commit()
                    db.session.add(MediaPlaylist(playlist_id=playlist.id, media_id=media.id))
        db.session.commit()
        return True
