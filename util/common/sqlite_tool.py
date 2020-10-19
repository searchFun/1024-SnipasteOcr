import sqlite3

from descriptions import bool_exception


class SqliteTemplate:
    def __init__(self, db_name):
        self._conn = sqlite3.connect(db_name)
        self._cursor = self.__get_cursor()

    def __get_cursor(self):
        return self._conn.cursor()

    def close(self):
        self._cursor.close()
        self._conn.close()

    @bool_exception
    def create_table(self, sql, parameters=[]):
        self._cursor.execute(sql, parameters)
        self._conn.commit()

    @bool_exception
    def drop_table(self, sql):
        self._cursor.execute(sql)
        self._conn.commit()

    @bool_exception
    def insert(self, sql_statement, parameters=[]):
        self._cursor.execute(sql_statement, parameters)
        self._conn.commit()

    @bool_exception
    def insert_many(self, sql_statement, parameters: list):
        self._cursor.executemany(sql_statement, parameters)
        self._conn.commit()

    def select(self, sql: str, parameters=[]):
        result = []

        @bool_exception
        def select():
            cursor = self._cursor.execute(sql, parameters)
            for row in cursor:
                tmp = []
                for item in row:
                    tmp.append(item)
                result.append(tmp)

        select()
        return result

    @bool_exception
    def update(self, sql_statement, parameters=[]):
        self._cursor.execute(sql_statement, parameters)
        self._conn.commit()

    @bool_exception
    def delete(self, sql_statement, parameters=[]):
        self._cursor.execute(sql_statement, parameters)
        self._conn.commit()
