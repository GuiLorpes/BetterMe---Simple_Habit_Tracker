import sqlite3
from datetime import date
from enum import Enum, auto

def main():
    print('\n')
    


class Frequency(Enum):
    DAILY = 'Daily'
    WEEKLY = 'Weekly'

def get_connectiondb():
    connection = sqlite3.connect('habit.db')
    connection.row_factory = sqlite3.Row
    return connection

def get_habits():
    connection = get_connectiondb()
    habits_cursor = connection.execute('SELECT id, name, target, unit, frequency FROM Habits')
    habits = [dict(row) for row in habits_cursor]
    print('\nSeus habitos:\n---------------')
    for h in habits:
        hid, name, target, unit, frequency = h
        if frequency == Frequency.DAILY.value: 
            habits_cursor.execute("SELECT SUM(amount) FROM Logs WHERE habit_id=? AND date=?",
                                  (hid, str(date.today())),
                                  )
            total = habits_cursor.fetchone()[0] or 0
            print(f"{hid}. {name} – Today: {total}/{target} {unit}")
        elif frequency == Frequency.WEEKLY.value:
            habits_cursor.execute("SELECT SUM(amount) FROM Logs WHERE habit_id=? AND date>=date('now','-7 day')",
                                  (hid,),
                                  )
            total = habits_cursor.fetchone()[0] or 0
            print(f"{hid}. {name} – This week: {total}/{target} {unit}")

def add_habit(name: str, target: int, unit: str, frequency: Frequency):
    connection = get_connectiondb()
    connection.execute('INSERT INTO Habits (name, target, unit, frequency) VALUES (?, ?, ?, ?)', 
                       (name, target, unit, frequency))
    connection.commit()
    connection.close()

def delete_habit(id: int):
    connection = get_connectiondb()
    connection.execute('DELETE FROM Habits WHERE id = ?', (id,))
    connection.commit()
    connection.close()