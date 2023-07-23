import logging
import os

import psycopg2
from psycopg2 import OperationalError

from .sreality_item import SrealityItem


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
                host='db',
                port='5432',
            )

            self.table_name = os.environ.get("DB_TABLE_NAME")

            self.cursor = self.connection.cursor()

            columns = "name text, image_url text"

            self.cursor.execute(
                f"CREATE TABLE IF NOT EXISTS {self.table_name} ({columns})"
            )
            self.connection.commit()

            self.cursor.execute(f"DELETE FROM {self.table_name}")

            self.logger.info(f"Connected to the database. Table {self.table_name} created if not exists.")
        except OperationalError as e:
            self.logger.error(f"Error connecting to the database: {e}")
            raise e



    def process_item(self, item: SrealityItem, spider):
        """Insert item into the database."""
        self.logger.info(f"Inserting item {item.name} into the database.")

        name = item.name
        image_url = item.image_url

        sql = f"""
        INSERT INTO {self.table_name} (name, image_url)
        VALUES (%s, %s)
        """

        self.cursor.execute(sql, (name, image_url))
        self.connection.commit()

        return item

    def close_spider(self, spider):
        """Disconnect from the database."""
        self.logger.info(f"Closing spider scrapped {spider.name}.")
        self.cursor.close()
        self.connection.close()
