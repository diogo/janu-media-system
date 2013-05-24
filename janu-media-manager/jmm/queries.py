from sqlalchemy.orm.query import Query
from models import Cover, MediaType, User, Module, MediaSource
from sqlalchemy import or_

def as_dict(_list):
    if _list:
        new_list = []
        for item in _list:
            new_list.append(item._asdict())
        return new_list
    return None

def get_media_types(db_session, user_email=None, system_user=None):
    media_types = db_session.query(MediaType.id, MediaType.name, Cover.url.label('cover_url'))\
                            .join(MediaType.cover).join(MediaType.media_sources)\
                            .join(MediaSource.user)\
                            .filter(or_(User.email == user_email,
                                        User.email == system_user)).distinct().all()
    return as_dict(media_types)

def get_media_sources(db_session):
    pass

def get_user(db_session, user_email, user_password=None):
    query = db_session.query(User.id, User.name, User.email, User.admin,
                             User.description, Cover.url.label('cover_url')).join(Cover)
    if user_password:
        user = query.filter(User.email == user_email, User.password == user_password).first()
    else:
        user = query.filter(User.email == user_email).first()
    if user:
        return user._asdict()
    else:
        return None

def get_users(db_session):
    users = db_session.query(User.id, User.name, User.email, User.admin,
                             Cover.url.label('cover_url')).join(Cover).all()
    return as_dict(users)