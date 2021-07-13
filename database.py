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
            UNM INTEGER default 0,
            NM INTEGER default 0,
            routine INTEGER default 0,
            Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )""")

        self.connection.commit()

        self.connection.close()

    def create_dungeon_tables(self, dungeon):


        self.cursor.execute(f"""
        CREATE TABLE {dungeon} (
            
            number_of_runs INTEGER default 0,
            win INTEGER default 0,
            loss INTEGER default 0,

            Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )""")

        self.connection.commit()
        self.connection.close()


    def initialize(self):

        t = datetime.date.today()
        today = t.strftime("%Y-%m-%d")
        print(today)
     
        self.cursor.execute("""
        INSERT OR IGNORE INTO game_data(date, UNM, NM, routine) VALUES (CURRENT_DATE, 0, 0, 0)
        """)
   
        self.connection.commit()
        #self.connection.close()
        #self.connection.close()
        #self.cursor.execute("INSERT INTO game_data(date, UNM) VALUES(CURRENT_DATE , 1)")

    def select_data(self):

        self.cursor.execute("""
        SELECT * FROM game_data WHERE Timestamp>=date('now', 'start of day')
        """)
        d =  self.cursor.fetchall()
        print(d)

    def update_value(self, column, value=1):

        t = datetime.date.today()
        today = t.strftime("%Y-%m-%d")
        print(today)
     
        self.cursor.execute("UPDATE game_data SET {0} = {1} WHERE Timestamp>=date('now', 'start of day')".format(column, value))
   
        self.connection.commit()
        #self.connection.close()
        #self.connection.close()
        #self.cursor.execute("INSERT INTO game_data(date, UNM) VALUES(CURRENT_DATE , 1)")

    def insert_datum(self):

        today = datetime.date.today()
        self.cursor.execute(f"INSERT OR IGNORE INTO game_data(date) VALUES({today})")

    def get_posts(self, difficulty):
        with self.connection:
            self.cursor.execute(f"SELECT {difficulty} FROM game_data WHERE Timestamp>=date('now', 'start of day')")
            d =  self.cursor.fetchall()
            #print(d)
            #print(d[0][0])
            try:
                return d[0][0]

            except:
                print('index out fo range')

#d = DataBaseManager()

#d.create_table()
#d.initialize()
#d.update_value('NM', 0)
#d.insert_datum()

#d.select_data()

#d.get_posts('UNM')