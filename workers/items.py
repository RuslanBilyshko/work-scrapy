from scrapy.item import Item, Field


class ResumeItem(Item):
    id = Field()
    name = Field()
    url = Field()
    data = Field()
