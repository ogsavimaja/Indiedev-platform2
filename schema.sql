CREATE TABLE Users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    salt TEXT NOT NULL,
    hashed_password TEXT NOT NULL,
    email TEXT
);

CREATE TABLE Announcements (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES Users(id),
    title TEXT NOT NULL,
    about TEXT NOT NULL,
    download_link TEXT,
    intented_price INTEGER,
    intented_age_restriction INTEGER,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT
);

CREATE TABLE Classes (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    value TEXT NOT NULL
);

CREATE TABLE Class_types (
    id INTEGER PRIMARY KEY,
    class_title TEXT NOT NULL REFERENCES Classes(title),
    type TEXT NOT NULL
);

CREATE TABLE Announcement_classes (
    id INTEGER PRIMARY KEY,
    announcement_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    value TEXT NOT NULL
);
