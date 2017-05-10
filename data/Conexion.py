import sqlite3


class Conexion():

    def __init__(self, database='database.db'):
        self.database = database
        self.connect()
        statement=('CREATE TABLE IF NOT EXISTS Tweets (id INTEGER, screen_name TEXT, comment TEXT);')
        self.execute(statement)
        self.close()

    def connect(self):
        # Conecta con la base de datos SQLite3
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()

    def close(self): 
        # Cierra la base de datos SQLite3
        self.connection.commit()
        self.connection.close()
        self.connected = False

    def execute(self, sSQL):
        queries = []
        self.cursor.execute(sSQL)
        # Regresa los valores consultados
        data = self.cursor.fetchall()
        if sSQL.upper().startswith('SELECT'):
            #append query results
            queries.append(data)
        return queries


