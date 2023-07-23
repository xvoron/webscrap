import logging
import os

from flask import Flask, render_template

from db_wrapper import DBWrapper


app = Flask(__name__)
table_name = os.getenv('DB_TABLE_NAME')
logger = logging.getLogger(__name__)


def init_db():
    try:
        return DBWrapper(
                db_name=os.environ.get('POSTGRES_DB'),
                user=os.environ.get('POSTGRES_USER'),
                password=os.environ.get('POSTGRES_PASSWORD'),
                host='db',
                port='5432',
                )
    except Exception as e:
        logger.error(f'Failed to connect to db: {e}')
        return None


def get_data():
    with open('data.txt', 'r') as f:
        data = f.read()
        data = data.split('\n')
        data = [x.split(';') for x in data]
    return data


@app.route('/')
def index():
    logger.info('Request received')
    db = init_db()
    if db is None:
       logger.error('Failed to connect to db') 
       return render_template('failed.html')
    data = db.read_all(table_name)
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8080)
