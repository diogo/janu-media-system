from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from httplib import HTTPSConnection
import json
import hashlib

db = SQLAlchemy()

class Cover(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	url = db.Column(db.Text, unique=True)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.Text, nullable=False)
	email = db.Column(db.Text, unique=True, nullable=False)
	password = db.Column(db.Text, nullable=False)
	admin = db.Column(db.Boolean, nullable=False, default=False)
	description = db.Column(db.Text)

	cover_id = db.Column(db.Integer, db.ForeignKey('cover.id'), default=1)

	cover = relationship('Cover', uselist=False)

class Module(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.Text, nullable=False)

class MediaSource(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.Text)

	cover_id = db.Column(db.Integer, db.ForeignKey('cover.id'), default=1)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	module_id = db.Column(db.Integer, db.ForeignKey('module.id'), nullable=False)

	cover = relationship('Cover', uselist=False)
	user = relationship('User', uselist=False)
	module = relationship('Module', uselist=False)

class MediaType(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.Text, nullable=False)

	cover_id = db.Column(db.Integer, db.ForeignKey('cover.id'), default=1)

	cover = relationship('Cover', uselist=False)

class ContentType(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.Text, nullable=False)

	type_id = db.Column(db.Integer, db.ForeignKey('media_type.id'), nullable=False)

	media_type = relationship('MediaType', uselist=False)

class Media(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	url = db.Column(db.Text, nullable=False)
	date = db.Column(db.DateTime)
	content = db.Column(db.Text)
	name = db.Column(db.Text)
	play_counter = db.Column(db.Integer, default=0)

	cover_id = db.Column(db.Integer, db.ForeignKey('cover.id'), default=1)
	artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
	source_id = db.Column(db.Integer, db.ForeignKey('media_source.id'), nullable=False)
	content_type_id = db.Column(db.Integer, db.ForeignKey('content_type.id'), nullable=False)

	cover = relationship('Cover', uselist=False)
	artist = relationship('Artist', uselist=False)
	source = relationship('MediaSource', uselist=False)
	content_type = relationship('ContentType', uselist=False)

class Artist(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.Text, unique=True)
	content = db.Column(db.Text)

	cover_id = db.Column(db.Integer, db.ForeignKey('cover.id'), default=1)

	cover = relationship('Cover', uselist=False)
	
class Genre(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.Text, unique=True)
	content = db.Column(db.Text)

	cover_id = db.Column(db.Integer, db.ForeignKey('cover.id'), default=1)

	cover = relationship('Cover', uselist=False)

class Playlist(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.Text, nullable=False)
	public = db.Column(db.Boolean, nullable=False, default=False)
	collection = db.Column(db.Boolean, nullable=False, default=False)
	date = db.Column(db.DateTime)
	content = db.Column(db.Text)

	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	cover_id = db.Column(db.Integer, db.ForeignKey('cover.id'), default=1)

	cover = relationship('Cover', uselist=False)
	user = relationship('User', uselist=False)

class FavoriteMedia(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	media_id = db.Column(db.Integer, db.ForeignKey('media.id'), nullable=False)

class FavoritePlaylist(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	collection_position = db.Column(db.Integer)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.id'), nullable=False)

class MediaPlaylist(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	media_id = db.Column(db.Integer, db.ForeignKey('media.id'), nullable=False)
	playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.id'), nullable=False)

class MediaGenre(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	media_id = db.Column(db.Integer, db.ForeignKey('media.id'), nullable=False)
	genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'), nullable=False)
