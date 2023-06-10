import scrapy
import json
import logging
from ..items import LuxonisScraperItem

logging.getLogger("scrapy").setLevel(logging.ERROR)


class SrealitySpider(scrapy.Spider):
    name = "sreality"
    allowed_domains = ["www.sreality.cz"]
    start_urls = [
        "https://www.sreality.cz/api/cs/v2/estates?category_main_cb=1&category_type_cb=1&per_page=500&tms=1686203319961"
    ]

    def parse(self, response):
        response = json.loads(response.text)

        estates = response["_embedded"]["estates"]
        for estate in estates:
            item = LuxonisScraperItem()
            item["title"] = estate["name"]
            item["img_url"] = estate["_links"]["images"][0]["href"]

            yield item
