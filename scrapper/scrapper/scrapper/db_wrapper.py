import psycopg2


class DBWrapper:
    def __init__(self, db_name, user, password, host, port):
        self.connection = psycopg2.connect(
            dbname=db_name,
            user=user,
            password=password,
            host=host,
            port=port
            )

        self.cursor = self.connection.cursor()

    def create_table(self, table_name, columns):
        self.cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
            )
        self.connection.commit()

    def clear_table(self, table_name):
        self.cursor.execute(f"DELETE FROM {table_name} *")
        self.connection.commit()

    def insert(self, table_name, columns, values):
        self.cursor.execute(
            f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
            )
        self.connection.commit()

    def read_all(self, table_name):
        self.cursor.execute(f"SELECT * FROM {table_name}")
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()
