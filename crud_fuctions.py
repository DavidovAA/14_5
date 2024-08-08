import sqlite3
connection = sqlite3.connect('initiate.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Products(
id INT PRIMARY KEY,
title TEXT NOT NULL,
description TEXT,
price INT NOT NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INT PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INT NOT NULL,
balance INT NOT NULL
);
''')

def add_user(username, email, age):
    cursor.execute(f'''
    INSERT INTO Users (username, email, age, balance) VALUES('{username}', '{email}', '{age}', 1000)
    ''')
    connection.commit()

def is_included(username):
    check_username = cursor.execute('SELECT * FROM Users WHERE id=?', (username,))
    connection.commit()
    return username


connection.commit()
connection.close()
