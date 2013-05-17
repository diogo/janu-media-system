from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Media(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	source_id = db.Column(db.Integer, db.ForeignKey('media_source.id'), nullable=False)
	cover_id = db.Column(db.Integer, db.ForeignKey('cover.id'))
	url = db.Column(db.Text, nullable=False)
	date = db.Column(db.DateTime)
	content = db.Column(db.Text)
	name = db.Column(db.Text)

class MediaSource(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	type_id = db.Column(db.Integer, db.ForeignKey('media_type.id'), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	cover_id = db.Column(db.Integer, db.ForeignKey('cover.id'))
	module = db.Column(db.Text, nullable=False)
	name = db.Column(db.Text, nullable=False)
	exportable = db.Column(db.Boolean, nullable=False, default=False)

class MediaType(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	cover_id = db.Column(db.Integer, db.ForeignKey('cover.id'))
	name = db.Column(db.Text, unique=True, nullable=False)
	content = db.Column(db.Text)

class Artist(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	cover_id = db.Column(db.Integer, db.ForeignKey('cover.id'))
	name = db.Column(db.Text, unique=True)
	content = db.Column(db.Text)

class Genre(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	cover_id = db.Column(db.Integer, db.ForeignKey('cover.id'))
	name = db.Column(db.Text, unique=True)
	content = db.Column(db.Text)

class Cover(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	url = db.Column(db.Text, unique=True, nullable=False)

class Playlist(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	cover_id = db.Column(db.Integer, db.ForeignKey('cover.id'))
	name = db.Column(db.Text, nullable=False)
	public = db.Column(db.Boolean, nullable=False, default=False)
	collection = db.Column(db.Boolean, nullable=False, default=False)
	date = db.Column(db.DateTime)
	content = db.Column(db.Text)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	cover_id = db.Column(db.Integer, db.ForeignKey('cover.id'))
	name = db.Column(db.Text, unique=True, nullable=False)
	email = db.Column(db.Text, unique=True, nullable=False)
	password = db.Column(db.Text, nullable=False)
	admin = db.Column(db.Boolean, nullable=False, default=False)
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
