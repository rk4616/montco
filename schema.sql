CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    assigned_to INTEGER REFERENCES USERS(ID),
    log TEXT,
    -- if 0 -> not started, 1 -> in progress, 2 -> completed
    status INTEGER NOT NULL DEFAULT 0
)