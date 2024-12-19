CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL
);

INSERT OR IGNORE INTO USERS (username, password, role) VALUES ('odysseus', 'horse', 'commander')