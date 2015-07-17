# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ProjectPipeline(object):
    def process_item(self, item, spider):
        return item


# Cassandra Pipeline
from cassandra.cluster import Cluster

class CassandraPipeline(object):

    def __init__(self, cassandra_keyspace):
        self.cassandra_keyspace = cassandra_keyspace

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            cassandra_keyspace=crawler.settings.get('CASSANDRA_KEYSPACE')
        )

    def open_spider(self, spider):
        cluster = Cluster()
        self.session = cluster.connect(self.cassandra_keyspace)
        # create scrapy_items table
        self.session.execute("CREATE TABLE IF NOT EXISTS " + self.cassandra_keyspace + ".scrapy_items ( item text, PRIMARY KEY (item))")

    # def close_spider(self, spider):

    def process_item(self, item, spider):
        self.session.execute("INSERT INTO scrapy_items (item) VALUES (%s)",[str(item)])
        # note...
        # session.execute("INSERT INTO foo (bar) VALUES (%s)", "blah")  # wrong
        # session.execute("INSERT INTO foo (bar) VALUES (%s)", ("blah"))  # wrong
        # session.execute("INSERT INTO foo (bar) VALUES (%s)", ("blah", ))  # right
        # session.execute("INSERT INTO foo (bar) VALUES (%s)", ["blah"])  # right
        return item