from typing import Iterator

import scrapy

from ..sreality_item import SrealityItem, get_item


class SrealitySpider(scrapy.Spider):
    name = 'srealitybot'

    per_page = 500
    url = (f"https://www.sreality.cz/api/cs/v2/estates?"
           f"category_main_cb=1&category_type_cb=1&per_page={per_page}")

    def start_requests(self):
        self.logger.info(f"Start scraping {self.url}")
        yield scrapy.Request(
                url=self.url, callback=self.parse, method='GET')

    def parse(self, response) -> Iterator[SrealityItem]:
        data = response.json()
        data = data['_embedded']['estates']
        for item in data:
            yield get_item(item)
