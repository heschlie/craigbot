# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from scrapy.exporters import BaseItemExporter
import json


class FindPartsPipeline(object):

    def __init__(self):
        self.years = [
            '2005',
            '2006',
            '2007',
            '05',
            '06',
            '07',
        ]
        self.parts = [
            'downpipe',
            'down pipe',
            'uppipe',
            'up pipe',
            'headers',
            'header',
        ]

    def process_item(self, item, spider):

        if not any([year in item['title'] for year in self.years]):
            raise DropItem('Not correct year')
        # if not any([part in item['title'] for part in self.parts]):
            # raise DropItem('Not correct part')

        return item


class MyJSONExporter(BaseItemExporter):

    def __init__(self, file, **kwargs):
        self.file = file
        self._configure(kwargs, dont_fail=True)
        self.items = {}

    def start_exporting(self):
        pass

    def finish_exporting(self):
        item_json = json.dumps(self.items, indent=4, sort_keys=True)
        item_bytes = str.encode(item_json)
        self.file.write(item_bytes)

    def export_item(self, item):
        self.items[item['title']] = item['link']
