from connections import RDBConnection

class RDBClient:
    def __init__(self, database, **kwargs):
        self.rdb = RDBConnection(
            database,
            user=kwargs["user"],
            password=kwargs["password"],
            host=kwargs["host"],
            port=kwargs["port"],
        ).get_connection()

    def _get_client(self):
        return self.rdb

    def _create_tables(self, models):
        self.rdb.create_tables(models)