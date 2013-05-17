from sqlalchemy.orm.query import Query
from models import *
from sqlalchemy import or_

get_media_types = Query(entities=[MediaType.id, MediaType.name, Cover.url])\
			.filter(or_(User.email == 'diogo', User.email == 'system'),
				MediaType.cover_id == Cover.id,
				User.id == MediaSource.user_id,
				MediaSource.type_id == MediaType.id).distinct()