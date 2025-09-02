import sqlite3
from datetime import date
from enum import Enum, auto

class Frequency(Enum):
    DAILY = auto()
    WEEKLY = auto()

def get_connectiondb():
    connection = sqlite3.connect('habit.db')
    connection.row_factory = sqlite3.Row
    return connection

def add_habit(name: str, target: int, unit: str, frequency: )