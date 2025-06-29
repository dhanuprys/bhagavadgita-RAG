import os
import mysql.connector
from mysql.connector import pooling, errorcode


class MysqlClient:
    def __init__(
        self,
        host=None,
        port=None,
        user=None,
        password=None,
        database=None,
        pool_name="mypool",
        pool_size=5,
        charset="utf8mb4",
    ):
        # Read from env if not provided
        self.config = {
            "host": host or os.getenv("DB_HOST", "localhost"),
            "port": port or int(os.getenv("DB_PORT", 3306)),
            "user": user or os.getenv("DB_USER", "root"),
            "password": password or os.getenv("DB_PASS", "root"),
            "database": database or os.getenv("DB_NAME", "bhagavadgita"),
            "charset": charset,
        }
        self.pool = pooling.MySQLConnectionPool(
            pool_name=pool_name,
            pool_size=pool_size,
            pool_reset_session=True,
            **self.config,
        )

    def _get_conn(self):
        try:
            conn = self.pool.get_connection()
            if not conn.is_connected():
                conn.reconnect(attempts=3, delay=2)
            return conn
        except mysql.connector.Error as e:
            print(f"[MySQL] Error getting connection: {e}")
            raise

    def query(self, sql, params=None, dict_cursor=True):
        """
        Execute a `SELECT` (or other) and return all rows.
        """
        conn = self._get_conn()
        cursor = conn.cursor(dictionary=dict_cursor)
        try:
            cursor.execute(sql, params or ())
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def execute(self, sql, params=None):
        """
        Execute INSERT/UPDATE/DELETE. Returns affected rowcount.
        """
        conn = self._get_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, params or ())
            conn.commit()
            return cursor.rowcount
        finally:
            cursor.close()
            conn.close()
