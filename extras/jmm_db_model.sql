PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE cover (
	id INTEGER NOT NULL, 
	url TEXT NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (url)
);
CREATE TABLE media_type (
	id INTEGER NOT NULL, 
	cover_id INTEGER, 
	name TEXT NOT NULL, 
	content TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(cover_id) REFERENCES cover (id), 
	UNIQUE (name)
);
CREATE TABLE artist (
	id INTEGER NOT NULL, 
	cover_id INTEGER, 
	name TEXT, 
	content TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(cover_id) REFERENCES cover (id), 
	UNIQUE (name)
);
CREATE TABLE user (
	id INTEGER NOT NULL, 
	cover_id INTEGER, 
	name TEXT NOT NULL, 
	email TEXT NOT NULL, 
	password TEXT NOT NULL, 
	admin BOOLEAN NOT NULL, 
	content TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(cover_id) REFERENCES cover (id), 
	UNIQUE (name), 
	UNIQUE (email), 
	CHECK (admin IN (0, 1))
);
CREATE TABLE genre (
	id INTEGER NOT NULL, 
	cover_id INTEGER, 
	name TEXT, 
	content TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(cover_id) REFERENCES cover (id), 
	UNIQUE (name)
);
CREATE TABLE playlist (
	id INTEGER NOT NULL, 
	user_id INTEGER, 
	cover_id INTEGER, 
	name TEXT NOT NULL, 
	public BOOLEAN NOT NULL, 
	collection BOOLEAN NOT NULL, 
	date DATETIME, 
	content TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES user (id), 
	FOREIGN KEY(cover_id) REFERENCES cover (id), 
	CHECK (public IN (0, 1)), 
	CHECK (collection IN (0, 1))
);
CREATE TABLE media_source (
	id INTEGER NOT NULL, 
	type_id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	cover_id INTEGER, 
	module TEXT NOT NULL, 
	name TEXT NOT NULL, 
	exportable BOOLEAN NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(type_id) REFERENCES media_type (id), 
	FOREIGN KEY(user_id) REFERENCES user (id), 
	FOREIGN KEY(cover_id) REFERENCES cover (id), 
	CHECK (exportable IN (0, 1))
);
CREATE TABLE favorite_playlists (
	id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	playlist_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES user (id), 
	FOREIGN KEY(playlist_id) REFERENCES playlist (id)
);
CREATE TABLE media (
	id INTEGER NOT NULL, 
	source_id INTEGER NOT NULL, 
	cover_id INTEGER, 
	url TEXT NOT NULL, 
	date DATETIME, 
	content TEXT, 
	name TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(source_id) REFERENCES media_source (id), 
	FOREIGN KEY(cover_id) REFERENCES cover (id)
);
CREATE TABLE media_artists (
	id INTEGER NOT NULL, 
	media_id INTEGER NOT NULL, 
	artist_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(media_id) REFERENCES media (id), 
	FOREIGN KEY(artist_id) REFERENCES artist (id)
);
CREATE TABLE media_genres (
	id INTEGER NOT NULL, 
	media_id INTEGER NOT NULL, 
	genre_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(media_id) REFERENCES media (id), 
	FOREIGN KEY(genre_id) REFERENCES genre (id)
);
CREATE TABLE favorite_medias (
	id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	media_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES user (id), 
	FOREIGN KEY(media_id) REFERENCES media (id)
);
COMMIT;
