import sqlite3

connection = sqlite3.connect('db/t_history.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()
connection.close()
