DROP TABLE IF EXISTS temperatures;

CREATE TABLE temperatures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time TEXT,
    room_temp REAL,
    heater_temp REAL
);