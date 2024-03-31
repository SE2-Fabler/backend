DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS story;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    name TEXT,
    email TEXT
);

CREATE TABLE story (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    genre TEXT,
    bookmarks INTEGER,
    bookmarked BOOLEAN,
    FOREIGN KEY (author_id) REFERENCES user (id)
);