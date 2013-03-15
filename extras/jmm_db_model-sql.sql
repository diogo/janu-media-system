/* SQLEditor (SQLite)*/
DROP TABLE genre_media_item;
DROP TABLE playlist_media_item;
DROP TABLE media;
DROP TABLE album;
DROP TABLE artist;
DROP TABLE cover;
DROP TABLE genre;
DROP TABLE media_format_module;
DROP TABLE media_source;
DROP TABLE media_source_module;
DROP TABLE remote_control;
DROP TABLE text_content_module;
DROP TABLE playlist;
DROP TABLE user;

CREATE TABLE cover
(
id INTEGER NOT NULL PRIMARY KEY,
image BLOB NOT NULL
);

CREATE TABLE album
(
id INTEGER NOT NULL PRIMARY KEY,
cover_id INTEGER REFERENCES cover (id),
name TEXT NOT NULL
);

CREATE TABLE artist
(
id INTEGER NOT NULL PRIMARY KEY,
cover_id INTEGER REFERENCES cover (id),
name TEXT NOT NULL
);

CREATE TABLE genre
(
id INTEGER NOT NULL PRIMARY KEY,
name TEXT NOT NULL
);

CREATE TABLE media_format_module
(
id INTEGER NOT NULL PRIMARY KEY,
name TEXT NOT NULL
);

CREATE TABLE genre_media_item
(
genre_id INTEGER REFERENCES genre (id),
item_id INTEGER REFERENCES media (id)
);

CREATE TABLE media
(
id INTEGER NOT NULL PRIMARY KEY,
media_source_id INTEGER NOT NULL REFERENCES media_source (id),
format_module_id INTEGER NOT NULL REFERENCES media_format_module (id),
artist_id INTEGER REFERENCES artist (id),
author_id INTEGER REFERENCES artist (id),
album_id INTEGER REFERENCES album (id),
cover_id INTEGER REFERENCES cover (id),
text_content TEXT,
name TEXT
);

CREATE TABLE media_source_module
(
id INTEGER NOT NULL PRIMARY KEY,
name TEXT NOT NULL
);

CREATE TABLE media_source
(
id INTEGER NOT NULL PRIMARY KEY,
module_id INTEGER NOT NULL REFERENCES media_source_module (id),
name TEXT NOT NULL,
exportable INTEGER NOT NULL
);

CREATE TABLE playlist_media_item
(
media_id INTEGER REFERENCES media (id),
playlist_id INTEGER REFERENCES playlist (id)
);

CREATE TABLE remote_control
(
enable INTEGER NOT NULL
);

CREATE TABLE text_content_module
(
id INTEGER NOT NULL PRIMARY KEY,
name TEXT NOT NULL
);

CREATE TABLE user
(
id INTEGER NOT NULL PRIMARY KEY,
name TEXT NOT NULL,
email TEXT NOT NULL,
password TEXT NOT NULL
);

CREATE TABLE playlist
(
id INTEGER NOT NULL PRIMARY KEY,
user_id INTEGER NOT NULL REFERENCES user (id),
name TEXT NOT NULL
);

