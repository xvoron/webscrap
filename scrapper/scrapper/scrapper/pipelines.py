import io
import logging
import os
from typing import Optional

import psycopg2
from psycopg2 import OperationalError
import requests

from .sreality_item import SrealityItem


logging.basicConfig(format='%(levelname)s: [%(asctime)s] [%(name)s:%(lineno)d-%(funcName)20s()] %(message)s',
                    level=logging.ERROR, datefmt='%d/%m/%Y %I:%M:%S')


class ScrapperPipeline:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def open_spider(self, spider):
        """Connect to the database."""
        try:
            self.connection = psycopg2.connect(
                dbname=os.environ.get('POSTGRES_DB'),
                user=os.environ.get('POSTGRES_USER'),
                password=os.environ.get('POSTGRES_PASSWORD'),
                host=os.environ.get('POSTGRES_HOST'),
                port=os.environ.get('POSTGRES_PORT'),
            )

            self.table_name = os.environ.get("DB_TABLE_NAME")

            self.cursor = self.connection.cursor()

            columns = "name text, image_url text, image bytea"

            # Delete table if exists
            self.cursor.execute(f"DROP TABLE IF EXISTS {self.table_name}")
            self.connection.commit()

            self.cursor.execute(
                f"CREATE TABLE IF NOT EXISTS {self.table_name} ({columns})"
            )
            self.connection.commit()

            self.cursor.execute(f"DELETE FROM {self.table_name}")
            self.connection.commit()

            self.logger.info(f"Connected to the database. Table {self.table_name} created if not exists.")
        except OperationalError as e:
            self.logger.error(f"Error connecting to the database: {e}")
            raise e

    def process_item(self, item: SrealityItem, spider):
        """Insert item into the database."""
        self.logger.info(f"Inserting item {item.name} into the database.")

        name = item.name
        image_url = item.image_url
        image = self._get_image(image_url)

        sql = f"""
        INSERT INTO {self.table_name} (name, image_url, image)
        VALUES (%s, %s, %s)
        """

        self.cursor.execute(sql, (name, image_url, psycopg2.Binary(image.read() if image else b'')))
        self.connection.commit()
        return item

    def close_spider(self, spider):
        """Disconnect from the database."""
        self.logger.info(f"Closing spider scrapped {spider.name}.")
        self.cursor.close()
        self.connection.close()

    def _get_image(self, image_url: str) -> Optional[io.BytesIO]:
        """Get image from the url."""
        try:
            response = requests.get(image_url)

            if response.status_code == 200:
                image_bytes = io.BytesIO(response.content)
                return image_bytes
            else:
                self.logger.info(f"Failed to download image. Status code: {response.status_code}")

        except Exception as e:
            self.logger.error(f"Error occurred: {e}")
