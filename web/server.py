import io
import logging
import os

from PIL import Image
import psycopg2

from flask import Flask, render_template


logging.basicConfig(format='%(levelname)s: [%(asctime)s] [%(name)s:%(lineno)d-%(funcName)20s()] %(message)s',
                    level=logging.ERROR, datefmt='%d/%m/%Y %I:%M:%S')


class SrealityApp(Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._logger = logging.getLogger(__name__)
        self.table_name = os.getenv('DB_TABLE_NAME')
        self._data = None


        self.add_url_rule('/', 'index', self.index)
        self.add_url_rule('/image/<int:image_id>', 'get_image', self.get_image)

    def get_data(self):
        db_connection = self.get_db_connection()
        if db_connection is None:
            self._logger.error('Failed to connect to db')
            return render_template('failed.html')

        cursor = db_connection.cursor()
        cursor.execute(f"SELECT * FROM {self.table_name}")
        data = cursor.fetchall()
        self._data = data
        return data

    def index(self):
        data = self.get_data()
        return render_template('index.html', data=data)

    def get_image(self, image_id):
        if self._data is None:
            self.get_data()
        assert self._data is not None

        item = self._data[image_id]
        image = item[2]
        return self._load_image(image)

    def _load_image(self, image_bytes):
        pil_image = Image.open(io.BytesIO(image_bytes))
        imb_byte_array = io.BytesIO()
        pil_image.save(imb_byte_array, format='JPEG')
        imb_byte_array = imb_byte_array.getvalue()
        return imb_byte_array, 200, {'Content-Type': 'image/jpeg'}


    def get_db_connection(self):
        try:
            return psycopg2.connect(
                    dbname=os.environ.get('POSTGRES_DB'),
                    user=os.environ.get('POSTGRES_USER'),
                    password=os.environ.get('POSTGRES_PASSWORD'),
                    host=os.environ.get('POSTGRES_HOST'),
                    port=os.environ.get('POSTGRES_PORT'),
                    )
        except Exception as e:
            self._logger.error(f'Failed to connect to db: {e}')
            return None


if __name__ == '__main__':
    app = SrealityApp(__name__)
    app.run(
        host='0.0.0.0',
        port=8080)
