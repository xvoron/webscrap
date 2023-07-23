from db_wrapper import DBWrapper
import os


def init_db():
    try:
        return DBWrapper(
                db_name=os.environ.get('POSTGRES_DB'),
                user=os.environ.get('POSTGRES_USER'),
                password=os.environ.get('POSTGRES_PASSWORD'),
                host=os.environ.get('db'),
                port=os.environ.get('5432')
                )
    except Exception as e:
        print(e)
        return None

db = init_db()
table_name = os.getenv('DB_TABLE_NAME')

print(db.read_all(table_name))
