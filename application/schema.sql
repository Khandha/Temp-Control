DROP TABLE IF EXISTS temperatures;

CREATE TABLE temperatures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time TEXT,
    room_temp REAL,
    heater_temp REAL
);

CREATE TABLE set_temperatures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    set_temp REAL,
    time TEXT
)