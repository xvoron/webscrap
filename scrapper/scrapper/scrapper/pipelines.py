# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from db_wrapper import DBWrapper
from sreality_item import SrealityItem


class ScrapperPipeline:
    def open_spider(self, spider):
        """Connect to the database."""
        self.db = DBWrapper(
            db_name="sreality",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
            )
        self.db.create_table(table_name="sreality",
                             columns=("id SERIAL PRIMARY KEY, "
                                      "name text, "
                                      "image_url text"))

        self.db.clear_table(table_name="sreality")



    def process_item(self, item: SrealityItem, spider):
        """Insert item into the database."""
        self.db.insert(table_name="sreality",
                       columns="name, image_url",
                       values=f"'{item.name}', '{item.image_url}'")
        return item

    def close_spider(self, spider):
        """Disconnect from the database."""
        self.db.close()
