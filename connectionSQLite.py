import sqlite3

class Connect():
    def __init__(self):
        self.connection = sqlite3.connect('data.db')
        self.cursor = self.connection.cursor()
        
    def execute(self, sql):
        self.cursor.execute(sql)
        
    
    def close(self):
        self.connection.close()




