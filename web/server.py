import logging
import os

from flask import Flask, render_template
import psycopg2


app = Flask(__name__)
table_name = os.getenv('DB_TABLE_NAME')
logger = logging.getLogger(__name__)


def get_db_connection():
    try:
        return psycopg2.connect(
                dbname=os.environ.get('POSTGRES_DB'),
                user=os.environ.get('POSTGRES_USER'),
                password=os.environ.get('POSTGRES_PASSWORD'),
                host=os.environ.get('POSTGRES_HOST'),
                port=os.environ.get('POSTGRES_PORT'),
                )
    except Exception as e:
        logger.error(f'Failed to connect to db: {e}')
        return None


@app.route('/')
def index():
    logger.info('Request received')
    connection = get_db_connection()
    if connection is None:
       logger.error('Failed to connect to db')
       return render_template('failed.html')

    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")

    logger.info(f"Pull data from table {table_name}")
    data = cursor.fetchall()

    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8080)
