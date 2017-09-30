from scrapy.item import Item, Field


class WorkerItem(Item):
    name = Field()
