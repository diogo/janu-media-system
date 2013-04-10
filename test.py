#!/usr/bin/env python

from flask import Flask
#from flask.ext import restful.Api
#from jmm.models import db, DATABASE_URI
from jmm.models import *
#from jmm.rest_api import add_resources
from sqlalchemy import or_

app = Flask(__name__)
#api = restful.Api(app)
#add_resources(api)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
db.init_app(app)
db.app = app
#db.create_all()

#db.session.add(Cover(url='aa'))
#db.session.add(MediaType(name='musicas', cover_id=1))
#db.session.add(User(name='system', email='system', password='system'))
#db.session.add(User(name='diogo', email='diogo', password='diogo'))
#db.session.add(MediaSource(type_id=2, user_id=2, module='media_fire', name='Media Fire SD'))
#db.session.commit()

print db.session.query(MediaType.id, MediaType.name, Cover.url)\
		.filter(or_(MediaType.cover_id == Cover.id, MediaType.cover_id == None),
				or_(User.email == 'diogo', User.email == None),
				User.id == MediaSource.user_id,
				MediaSource.type_id == MediaType.id\
				).distinct().as_scalar()

#if __name__ == '__main__':
#    app.run(debug=True, ssl_context='adhoc')
