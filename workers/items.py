from scrapy.item import Item, Field


class ResumeListItem(Item):
    title = Field()
    name = Field()
    link = Field()
