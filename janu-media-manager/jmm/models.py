from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import UserMixin
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class Cover(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	url = db.Column(db.Text, unique=True)

class MediaType(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	cover_id = db.Column(db.Integer, db.ForeignKey('cover.id'), default=1)
	cover = relationship('Cover', uselist=False)
	name = db.Column(db.Text, unique=True, nullable=False)
	description = db.Column(db.Text)
	media_sources = relationship('MediaSource', backref='media_source')

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	cover_id = db.Column(db.Integer, db.ForeignKey('cover.id'), default=1)
	name = db.Column(db.Text, nullable=False)
	email = db.Column(db.Text, unique=True, nullable=False)
	password = db.Column(db.Text, nullable=False)
	admin = db.Column(db.Boolean, nullable=False, default=False)
	description = db.Column(db.Text)

class Module(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.Text, nullable=False)

class MediaSource(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	type_id = db.Column(db.Integer, db.ForeignKey('media_type.id'), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	cover_id = db.Column(db.Integer, db.ForeignKey('cover.id'), default=1)
	module_id = db.Column(db.Integer, db.ForeignKey('module.id'), nullable=False)
	type = relationship('MediaType', uselist=False)
	cover = relationship('Cover', uselist=False)
	user = relationship('User', uselist=False)
	module = relationship('Module', uselist=False)
	name = db.Column(db.Text, nullable=False)
	exportable = db.Column(db.Boolean, nullable=False, default=False)

class MediaSourceMedia(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	media_source_id = db.Column(db.Integer, db.ForeignKey('media_source.id'), nullable=False)

class Media(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	source_id = db.Column(db.Integer, db.ForeignKey('media_source.id'), nullable=False)
	cover_id = db.Column(db.Integer, db.ForeignKey('cover.id'), default=1)
	url = db.Column(db.Text, nullable=False)
	date = db.Column(db.DateTime)
	content = db.Column(db.Text)
	name = db.Column(db.Text)

class Artist(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	cover_id = db.Column(db.Integer, db.ForeignKey('cover.id'), default=1)
	name = db.Column(db.Text, unique=True)
	content = db.Column(db.Text)

class Genre(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	cover_id = db.Column(db.Integer, db.ForeignKey('cover.id'), default=1)
	name = db.Column(db.Text, unique=True)
	content = db.Column(db.Text)

class Playlist(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	cover_id = db.Column(db.Integer, db.ForeignKey('cover.id'), default=1)
	name = db.Column(db.Text, nullable=False)
	public = db.Column(db.Boolean, nullable=False, default=False)
	collection = db.Column(db.Boolean, nullable=False, default=False)
	date = db.Column(db.DateTime)
	content = db.Column(db.Text)

class FavoriteMedias(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	media_id = db.Column(db.Integer, db.ForeignKey('media.id'), nullable=False)

class FavoritePlaylists(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.id'), nullable=False)

class MediaGenres(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	media_id = db.Column(db.Integer, db.ForeignKey('media.id'), nullable=False)
	genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'), nullable=False)

class MediaArtists(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	media_id = db.Column(db.Integer, db.ForeignKey('media.id'), nullable=False)
	artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
