/* SQLEditor (SQLite)*/
DROP TABLE cover_media;
DROP TABLE genre_media;
DROP TABLE playlist_media_item;
DROP TABLE media;
DROP TABLE album;
DROP TABLE artist;
DROP TABLE cover;
DROP TABLE genre;
DROP TABLE media_source;
DROP TABLE playlist;
DROP TABLE user;

CREATE TABLE album
(
id INTEGER NOT NULL PRIMARY KEY,
name TEXT NOT NULL
);

CREATE TABLE artist
(
id INTEGER NOT NULL PRIMARY KEY,
name TEXT NOT NULL
);

CREATE TABLE cover
(
id INTEGER NOT NULL PRIMARY KEY,
image BLOB NOT NULL
);

CREATE TABLE genre
(
id INTEGER NOT NULL PRIMARY KEY,
name TEXT NOT NULL
);

CREATE TABLE genre_media
(
genre_id INTEGER REFERENCES genre (id),
item_id INTEGER REFERENCES media (id)
);

CREATE TABLE cover_media
(
artist_id INTEGER REFERENCES artist (id),
media_id INTEGER REFERENCES media (id),
cover_id INTEGER NOT NULL REFERENCES cover (id),
album_id INTEGER REFERENCES album (id)
);

CREATE TABLE media
(
artist_id INTEGER REFERENCES artist (id),
author_id INTEGER REFERENCES artist (id),
media_source_id INTEGER NOT NULL REFERENCES media_source (id),
format TEXT NOT NULL,
id INTEGER NOT NULL PRIMARY KEY,
album_id INTEGER REFERENCES album (id),
kind TEXT NOT NULL,
url TEXT NOT NULL,
text_content TEXT,
name TEXT
);

CREATE TABLE playlist_media_item
(
media_id INTEGER REFERENCES media (id),
playlist_id INTEGER REFERENCES playlist (id)
);

CREATE TABLE user
(
id INTEGER NOT NULL PRIMARY KEY,
name TEXT NOT NULL,
email TEXT NOT NULL,
password TEXT NOT NULL
);

CREATE TABLE media_source
(
id INTEGER NOT NULL PRIMARY KEY,
user_id INTEGER NOT NULL REFERENCES user (id),
module TEXT NOT NULL,
name TEXT NOT NULL,
exportable INTEGER NOT NULL
);

CREATE TABLE playlist
(
id INTEGER NOT NULL PRIMARY KEY,
user_id INTEGER NOT NULL REFERENCES user (id),
name TEXT NOT NULL
);

