import sqlite3
from datetime import date
from enum import Enum, auto

def main():
    choice = 0
    while choice != 4:
        print('\n1 -> Adicionar Hábito\n2 -> Remover Hábito\n3 -> Verificar Hábitos\n4 -> Sair')
        choice = int(input('Escolha qual ação você deseja realizar:\n'))
        if choice == 1:
            habit_type = str(input('Are you trying to build a good habit, or break a bad one? (Build/Break)\n'))
            if habit_type == 'Build':
                habit = str(input('What habit are you building?\n'))
            if habit_type == 'Break':
                habit = str(input('What habit are you trying to break?\n'))
            goal = int(input("What's your goal?\n"))
            unit = str(input("What's your habits unit of measure?\n"))
            frequency = str(input("What's the frequency of your habit? (Daily/Weekly)\n"))
            add_habit(habit, goal, habit_type, unit, frequency)
        if choice == 2:
            habit = str()
        if choice == 3:
            get_habits()
        

class HabitType(Enum):
    BUILD = 'Build'
    BREAK = 'Break'

class Frequency(Enum):
    DAILY = 'Daily'
    WEEKLY = 'Weekly'

def format_goals(s: str) -> list[str]:
    '''
    Receives a goal string *s* and separate the number, the unit, and the frequency
    Examples
    >>> format_goal(50 pages/week)
    ['50', 'pages', 'week']
    '''
    goal = ''
    unit = ''
    frequency = ''
     

def get_connectiondb():
    connection = sqlite3.connect('habit.db')
    connection.row_factory = sqlite3.Row
    return connection

def get_habits():
    connection = get_connectiondb()
    habits_cursor = connection.execute('SELECT id, habit, goal, habit_type, unit, frequency FROM Habits')
    habits = [dict(row) for row in habits_cursor]
    if not habits:
        print("\nYou still don't have any habits:\n---------------")
    print('\nYour habits:\n---------------')
    for h in habits:
        hid = h['id']
        habit = h['habit']
        habit_type = h['habit_type']
        goal = h['goal']
        unit = h['unit']
        frequency = h['frequency']
        if frequency == Frequency.DAILY.value: 
            habits_cursor.execute("SELECT SUM(amount) FROM Logs WHERE habit_id=? AND date=?",
                                  (hid, str(date.today())),
                                  )
            total = habits_cursor.fetchone()[0] or 0
            print(f"{hid}. {habit} – Today: {total}/{goal} {unit}")
        elif frequency == Frequency.WEEKLY.value:
            habits_cursor.execute("SELECT SUM(amount) FROM Logs WHERE habit_id=? AND date>=date('now','-7 day')",
                                  (hid,),
                                  )
            total = habits_cursor.fetchone()[0] or 0
            print(f"{hid}. {habit} – This week: {total}/{goal} {unit}")

def add_habit(name: str, goal: int, habit_type: int,unit: str, frequency: Frequency):
    connection = get_connectiondb()
    connection.execute('INSERT INTO Habits (habit, goal, habit_type, unit,frequency) VALUES (?, ?, ?, ?, ?)', 
                       (name, goal, habit_type, unit, frequency))
    connection.commit()
    connection.close()

def delete_habit(id: int):
    connection = get_connectiondb()
    connection.execute('DELETE FROM Habits WHERE id = ?', (id,))
    connection.commit()
    connection.close()

if __name__ == '__main__':
    main()