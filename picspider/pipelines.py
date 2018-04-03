# -*- coding: utf-8 -*-
import urllib.request


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class PicspiderPipeline(object):
    def process_item(self, item, spider):
        pic_url = item['picurl']
        pic_id = item['picid'].replace("/","")
        local_path = "/home/mata/dataex/pics/" + pic_id + ".jpg"
        # print(local_path)
        urllib.request.urlretrieve(pic_url, filename=local_path)
        return item
