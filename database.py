import sqlite3
import datetime


class DataBaseManager():

    def __init__(self):

        self.connection = sqlite3.connect('data.db')
        self.cursor = self.connection.cursor()

    def create_table(self):


        self.cursor.execute("""
        CREATE TABLE game_data (
            date TEXT PRIMARY KEY,
            UNM BOOLEAN default 0,
            NM BOOLEAN default 0
        )""")

        self.connection.commit()

        self.connection.close()

    def insert_bolean(self, column):

        t = datetime.date.today()
        today = t.strftime("%Y-%m-%d")
        print(today)

        self.cursor.execute("""
        INSERT OR IGNORE INTO game_data(date, UNM) VALUES (CURRENT_DATE, 1)
        UPDATE game_data 
        SET UNM = 1 
        WHERE date= CURRENT_DATE
        """)
        self.connection.commit()
        #self.connection.close()
        #self.cursor.execute("INSERT INTO game_data(date, UNM) VALUES(CURRENT_DATE , 1)")
    def insert_datum(self):

        today = datetime.date.today()
        self.cursor.execute(f"INSERT INTO game_data(date) VALUES({today})")

    def get_posts(self):
        with self.connection:
            self.cursor.execute("SELECT * FROM game_data")
            print(self.cursor.fetchall())


d = DataBaseManager()

#d.create_table()

d.insert_bolean('UNM')
#d.insert_datum()

#d.get_posts()