import logging

import psycopg2


class DBWrapper:
    def __init__(self, db_name, user, password, host, port):
        self.logger = logging.getLogger(__name__)
        try:
            self.connection = psycopg2.connect(
                dbname=db_name,
                user=user,
                password=password,
                host=host,
                port=port
                )
            self.logger.info(f"Connected to the database. {self.connection}")
        except psycopg2.Error as e:
            self.logger.error(f"Error connecting to the database. {e}")
            raise e

        self.cursor = self.connection.cursor()

    def create_table(self, table_name, columns):
        self.logger.info(f"Creating table {table_name} with columns {columns}")
        self.cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
            )
        self.connection.commit()

    def clear_table(self, table_name):
        self.logger.info(f"Clearing table {table_name}")
        self.cursor.execute(f"DELETE FROM {table_name}")
        self.connection.commit()

    def insert(self, table_name, columns, values):
        self.logger.info(f"Inserting into table {table_name} with columns {columns} and values {values}")
        self.cursor.execute(
            f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
            )
        self.connection.commit()

    def read_all(self, table_name):
        self.logger.info(f"Reading all from table {table_name}")
        self.cursor.execute(f"SELECT * FROM {table_name}")
        return self.cursor.fetchall()

    def close(self):
        self.logger.info(f"Closing connection {self.connection}")
        self.cursor.close()
        self.connection.close()
