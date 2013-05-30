from sqlalchemy.orm.query import Query
from models import Cover, MediaType, User, Module, MediaSource, db
from sqlalchemy import or_

class DoQuery(object):
    def __init__(self, db_session):
        self._db_session = db_session

    def _as_dict(self, _list):
        if _list:
            new_list = []
            for item in _list:
                new_list.append(item._asdict())
            return new_list
        return None

    def get_user(self, user_email, user_password=None):
        query = self._db_session.query(User.id, User.name, User.email, User.admin,
                                       User.description, Cover.url.label('cover_url')).join(Cover)
        if user_password:
            user = query.filter(User.email == user_email, User.password == user_password).first()
        else:
            user = query.filter(User.email == user_email).first()
        if user:
            return user._asdict()
        else:
            return None

    def get_users(self):
        users = self._db_session.query(User.id, User.name, User.email, User.admin,
                                       Cover.url.label('cover_url')).join(Cover).all()
        return self._as_dict(users)

    def get_media_sources(self, user_email=None, system_user=None):
        media_sources = self._db_session.query(MediaSource.id, MediaSource.name,
                                               Cover.url.label('cover_url'),
                                               Module.name.label('module_name'))
        media_sources = media_sources.join(MediaSource.cover)\
                                     .join(MediaSource.module)\
                                     .join(MediaSource.user)
        media_sources = media_sources.filter(or_(User.email == user_email,
                                                 User.email == system_user)).distinct().all()
        return self._as_dict(media_sources)
