import sqlite3
from datetime import date

connection = sqlite3.connect('habit.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Habits (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               habit VARCHAR(100) NOT NULL,
               goal INTEGER NOT NULL,
               habit_type TINYINT(1) NOT NULL,
               unit VARCHAR(50) NOT NULL,
               frequency VARCHAR(20) NOT NULL)
               ''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Logs (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               habit_id INTEGER NOT NULL,
               amount INTEGER NOT NULL,
               date TEXT,
               FOREIGN KEY (habit_id) REFERENCES Habits.id
               ''')

print("Database and 'Habits' and 'Logs' tables have been created!")

connection.commit()
connection.close()