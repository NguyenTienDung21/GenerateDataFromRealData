import psycopg2
from psql.config import config

class PSQLconnector:
    def __init__(self):
        self.conn = None
        self.curr = None

    def connect(self):
        try:
            params = config()
            print(params)
            self.conn = psycopg2.connect(**params)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def execute(self, command, callback):
        try:
            self.curr = self.conn.cursor()
            self.curr.execute(command)
            row = self.curr.fetchone()
            while row is not None:
                callback(row)
                row = self.curr.fetchone()
            self.curr.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def disconnect(self):
        if self.conn is not None:
            self.conn.close()
