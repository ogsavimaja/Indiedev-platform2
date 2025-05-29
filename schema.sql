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
    intented_price INTEGER,
    intented_age_restriction INTEGER,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT
);
