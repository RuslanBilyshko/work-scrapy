# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, Text
from sqlalchemy.orm import Session
from sqlalchemy.sql import exists
import os

Base = declarative_base()


class ResumesTable(Base):
    __tablename__ = 'resumes'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    url = Column(String)
    data = Column(Text)

    def __init__(self, id, name, url, data):
        self.id = id
        self.name = name
        self.url = url
        self.data = data

    def __repr__(self):
        return "<Data %s, %s>" % (self.name, self.url)


class ResumePipeline(object):
    def __init__(self):
        basename = 'data_scraped'
        self.engine = create_engine("sqlite:///%s" % basename, echo=False)
        if not os.path.exists(basename):
            Base.metadata.create_all(self.engine)

        self.id = set()

    def process_item(self, item, spider):

        if not self.session.query(ResumesTable).filter(ResumesTable.id==item['id']).count():
            dt = ResumesTable(
                id=item['id'],
                name=item['name'],
                url=item['url'],
                data=item['data'],
            )
            self.session.add(dt)
        return item

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()

    def open_spider(self, spider):
        self.session = Session(bind=self.engine)