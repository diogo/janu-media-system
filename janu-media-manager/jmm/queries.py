from sqlalchemy.orm.query import Query
from models import Cover, MediaType, User, Module, MediaSource
from sqlalchemy import or_
from settings import SYSTEM_USER

def get_media_types(user_email, system_user=SYSTEM_USER):
	return Query(entities=[MediaType.id, MediaType.name, Cover.url])\
			.filter(or_(User.email == user_email, User.email == system_user),
				MediaType.cover_id == Cover.id,
				User.id == MediaSource.user_id,
				MediaSource.type_id == MediaType.id).distinct()

def get_user(db_session, user_email, user_password=None):
    if user_password:
        user = db_session.query(User.name, User.email, User.admin, User.description, Cover.url).join(Cover)\
                               .filter(User.email == user_email,
                                       User.password == user_password).first()
    else:
        user = db_session.query(User.name, User.email, User.admin, User.description, Cover.url).join(Cover)\
                               .filter(User.email == user_email).first()
    if user:
        return user._asdict()
    else:
        return None
    