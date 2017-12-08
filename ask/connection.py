import MySQLdb


class Connection:
    def __init__(self, host, db_name,db_user, db_pass, db_charset):
        self.host = host
        self.db_name = db_name
        self._connection = None
        self.db_user = db_user
        self.db_pass = db_pass
        self.db_charset = db_charset

    @property
    def connection(self):
        return self._connection

    def __enter__(self):
        return self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def connect(self):
        if not self._connection:
            self._connection = MySQLdb.connect(
                host=self.host,
                db=self.db_name,
                user=self.db_user,
                passwd=self.db_pass,
                charset=self.db_charset,
            )
            return self.connection

    def disconnect(self):
        if self._connection:
            self._connection.close()
