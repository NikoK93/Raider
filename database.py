import sqlite3
import datetime


class DataBaseManager():

    def __init__(self):

        self.connection = sqlite3.connect('data.db')
        self.cursor = self.connection.cursor()

    def create_table(self):

        self.cursor.execute("""
        CREATE TABLE game_data (
            date DATE,
            UNM BOOL,
            NM BOOL
        )""")

        self.connection.commit()

        self.connection.close()

    def insert(self, column):

        today = datetime.date.today()
        query = today
        self.cursor.execute(f"insert into game_data({column}) values (?)", query)

    

d = DataBaseManager()

d.insert('date')