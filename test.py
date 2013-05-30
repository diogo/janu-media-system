#!/usr/bin/env python
# -*- coding: utf-8 -*-

from jmm.models import db, User, Cover, Module, Mediafire, MediaType, Format
from jmm.service import application
from sys import argv
import hashlib

db.init_app(application)
db.app = application

if len(argv) > 1:
    if argv[1] == 'create':
        db.create_all()
        db.session.add(Cover())
        db.session.add(Cover(url='http://cdn1.iconfinder.com/data/icons/VISTA/database/png/400/administrator.png'))
        db.session.add(Module(name='mediafire'))
        db.session.add(Mediafire())
        db.session.add(User(name='system',
                            email='system',
                            password=hashlib.md5('system').hexdigest(),
                            admin=True,
                            cover_id=2))
        db.session.add(MediaType(name=u'Músicas'))
        db.session.add(Format(name='audio/mpeg', type_id=1))
        db.session.commit()


"""
#!/usr/bin/env python

from flask import Flask, request
#from flask.ext import restful.Api
#from jmm.models import db, DATABASE_URI
from jmm import queries
from jmm.models import *
#from jmm.rest_api import add_resources
from sqlalchemy import or_
from sqlalchemy.orm.query import Query

app = Flask(__name__)
#api = restful.Api(app)
#add_resources(api)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db.init_app(app)
db.app = app
#db.create_all()

for query in queries.values():
	query.session = db.session()
print queries['media_types'].all()

print db.session.query(MediaSource.type_id, MediaSource.name).all()
print db.session.query(MediaType.cover_id, MediaType.name, MediaType.id).all()
print db.session.query(User.cover_id, User.name, User.email, User.password).all()

@app.route('/user/', methods=['POST'])
def add_user():
	user = request.form
	if user.has_key('name') and user.has_key('email') and user.has_key('password'):
		pass
	else:
		return 'ERROR!'
	db.session.add(User(name=user['name'],
						email=user['email'],
						password=user['password']))
	try:
		db.session.commit()
	except:
		return 'ERROR!'
	return 'OK!'


if __name__ == '__main__':
    app.run()

"""
