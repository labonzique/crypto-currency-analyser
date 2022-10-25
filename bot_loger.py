import psycopg2
from psycopg2.extras import RealDictCursor
from auth import PostgreSqlConfig


class PgDriver:

    def __init__(self):
        self._dsn = PostgreSqlConfig.DATABASE_URL

    def __enter__(self):
        self.conn = psycopg2.connect(self._dsn, cursor_factory=RealDictCursor)
        self.curr = self.conn.cursor()

        return self.curr

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()
        self.curr.close()

