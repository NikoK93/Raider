import sqlite3
import datetime


class DataBaseManager():

    def __init__(self, account='raid3'):

        self.account = account

        self.connection = sqlite3.connect('data.db')
        self.cursor = self.connection.cursor()

    def create_table(self):


        self.cursor.execute("""
        CREATE TABLE {0} (
            date TEXT PRIMARY KEY,
            UNM INTEGER default 0,
            NM INTEGER default 0,
            routine INTEGER default 0,
            Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )""".format(self.account+"_states"))

        self.connection.commit()

        self.connection.close()

    def create_fw_table(self):


        self.cursor.execute("""
        CREATE TABLE {0} (
            dark_elves INTEGER default 1,
            sacred_order INTEGER default 1,
            banner_lords INTEGER default 1,
            barbarians INTEGER default 1,
            dwarfs INTEGER default 1,
            knight_revenant INTEGER default 1,
            lizardmen INTEGER default 1,
            skinwalkers INTEGER default 1,
            undead_horde INTEGER default 1,
            demonspawn INTEGER default 1,
            ogryn_tribe INTEGER default 1,
            orc INTEGER default 1,
            high_elves INTEGER default 1
        )""".format(self.account+"_FW "))


        self.connection.commit()
        self.connection.close()

    def create_leveling_table(self):


        self.cursor.execute("""
        CREATE TABLE {0} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run INTEGER default 0
        )""".format("AutoLeveler"))


        self.connection.commit()
        self.connection.close()

    def generic_update_value(self, column, value=1):


        self.cursor.execute("UPDATE {0} SET {1} = {2}".format(self.account+"_states", column, value))
   
        self.connection.commit()
        #self.connection.close()
        #self.connection.close()
        #self.cursor.execute("INSERT INTO game_data(date, UNM) VALUES(CURRENT_DATE , 1)")


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
        INSERT OR IGNORE INTO {0}(date, UNM, NM, routine) VALUES (CURRENT_DATE, 0, 0, 0)
        """.format(self.account+"_states"))
   
        self.connection.commit()
        #self.connection.close()
        #self.connection.close()
        #self.cursor.execute("INSERT INTO game_data(date, UNM) VALUES(CURRENT_DATE , 1)")

    def select_data(self):

        self.cursor.execute("""
        SELECT * FROM {0} WHERE Timestamp>=date('now', 'start of day')
        """.format(self.account+"_states"))
        d =  self.cursor.fetchall()
        print(d)

    def update_value(self, column, value=1):

        t = datetime.date.today()
        today = t.strftime("%Y-%m-%d")
        print(today)
     
        self.cursor.execute("UPDATE {0} SET {1} = {2} WHERE Timestamp>=date('now', 'start of day')".format(self.account+"_states", column, value))
   
        self.connection.commit()
        #self.connection.close()
        #self.connection.close()
        #self.cursor.execute("INSERT INTO game_data(date, UNM) VALUES(CURRENT_DATE , 1)")

    #def update_leveling_value(self, value):

     
    #    self.cursor.execute("INSERT INTO AutoLeveler VALUES ({0}, {1})".format(0, value))
    #    self.connection.commit()
    
    def update_leveling_value(self, value):

     
        self.cursor.execute("UPDATE AutoLeveler SET run = {0} WHERE id = 0".format(value))
        self.connection.commit()

    def get_levling_value(self):

        with self.connection:
            self.cursor.execute("SELECT * FROM AutoLeveler ORDER BY run DESC LIMIT 1")
            d =  self.cursor.fetchall()
            #print(d[0][1])
            try:
                return d[0][1]
            except:
                print('index out fo range')
            #self.connection.commit()

    def insert_datum(self):

        today = datetime.date.today()
        self.cursor.execute(f"INSERT OR IGNORE INTO game_data(date) VALUES({today})")

    def get_posts(self, difficulty):
        with self.connection:
            self.cursor.execute("SELECT {0} FROM {1} WHERE Timestamp>=date('now', 'start of day')".format(difficulty,self.account+"_states"))
            d =  self.cursor.fetchall()
            #print(d)
            #print(d[0][0])
            try:
                return d[0][0]

            except:
                print('index out fo range')

#d = DataBaseManager('raid3')


#d.create_leveling_table()

#d.get_levling_value()
#d.update_leveling_value(0)
#d.create_table()
#d.initialize()
#d.update_value('routine', 0)
#d.insert_datum()

#d.select_data()

#d.get_posts('routine')