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

	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	cover_id = db.Column(db.Integer, db.ForeignKey('cover.id'), default=1)
	module_id = db.Column(db.Integer, db.ForeignKey('module.id'), nullable=False)

	cover = relationship('Cover', uselist=False)
	user = relationship('User', uselist=False)
	module = relationship('Module', uselist=False)

class MediaType(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.Text, nullable=False)

	cover_id = db.Column(db.Integer, db.ForeignKey('cover.id'), default=1)

	cover = relationship('Cover', uselist=False)

class Format(db.Model):
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
	source_id = db.Column(db.Integer, db.ForeignKey('media_source.id'), nullable=False)
	format_id = db.Column(db.Integer, db.ForeignKey('format.id'), default=1)

	cover = relationship('Cover', uselist=False)
	source = relationship('MediaSource', uselist=False)
	format = relationship('Format', uselist=False)

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

class FavoriteMedias(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	media_id = db.Column(db.Integer, db.ForeignKey('media.id'), nullable=False)

class FavoritePlaylists(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.id'), nullable=False)

class MediaPlaylists(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	media_id = db.Column(db.Integer, db.ForeignKey('media.id'), nullable=False)
	playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.id'), nullable=False)

class MediaGenres(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	media_id = db.Column(db.Integer, db.ForeignKey('media.id'), nullable=False)
	genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'), nullable=False)

class MediaArtists(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	media_id = db.Column(db.Integer, db.ForeignKey('media.id'), nullable=False)
	artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
