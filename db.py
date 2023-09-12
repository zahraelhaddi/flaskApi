import sqlite3

connection = sqlite3.connect("books.sqlite")
# cursor ibject used to execute sql statements
cursor = connection.cursor()
sql_query = """CREATE TABLE book (
    id integer PRIMARY KEY,
    author text NOT NULL,
    language text NOT NULL,
    title text NOT NULL
    )"""

cursor.execute(sql_query)
