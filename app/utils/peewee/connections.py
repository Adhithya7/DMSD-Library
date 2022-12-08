from peewee import *


class RDBConnection:
    def __init__(self, database, user, password, host, port):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def get_connection(self):
        self.db = PostgresqlDatabase(
            self.database,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            autorollback=True,
        )
        self.db.connect()
        return self.db

