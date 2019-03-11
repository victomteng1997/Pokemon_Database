import sqlite3

conn = sqlite3.connect('pokemon.db')
c = conn.cursor()
c.execute("PRAGMA table_info(Pokemon_basic_data)")
column_info = c.fetchall()
t = ('pidgeotto',)
c.execute('SELECT * FROM Pokemon_basic_data WHERE name=?', t)
result = c.fetchone()

combine = {}
for i in range(0,len(column_info)):
    combine[column_info[i][1]] = result[i]

print(combine)