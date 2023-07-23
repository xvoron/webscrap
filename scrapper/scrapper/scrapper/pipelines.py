import logging
import os

from db_wrapper import DBWrapper
from sreality_item import SrealityItem


class ScrapperPipeline:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    def open_spider(self, spider):
        """Connect to the database."""
        self.db = DBWrapper(
            db_name=os.environ.get('POSTGRES_DB'),
            user=os.environ.get('POSTGRES_USER'),
            password=os.environ.get('POSTGRES_PASSWORD'),
            host=os.environ.get('db'),
            port=os.environ.get('5432')
            )
        self.table_name = os.environ.get("DB_TABLE_NAME")

        self.db.create_table(table_name=self.table_name,
                             columns=("id SERIAL PRIMARY KEY, "
                                      "name text, "
                                      "image_url text"))

        self.db.clear_table(table_name=self.table_name)



    def process_item(self, item: SrealityItem, spider):
        """Insert item into the database."""
        self.logger.info(f"Inserting item {item.name} into the database.")
        self.db.insert(table_name=self.table_name,
                       columns="name, image_url",
                       values=f"'{item.name}', '{item.image_url}'")
        return item

    def close_spider(self, spider):
        """Disconnect from the database."""
        self.logger.info(f"Closing spider scrapped {len(self.db.read_all(self.table_name))} items.")
        self.db.close()
