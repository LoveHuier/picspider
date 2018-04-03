# -*- coding: utf-8 -*-
import scrapy
import re
# import urllib.request

from picspider.items import PicspiderItem


class PicSpider(scrapy.Spider):
    name = 'pic'
    allowed_domains = ['mmjpg.com']
    start_urls = ('http://www.mmjpg.com/',)

    def parse(self, response):
        item = PicspiderItem()

        picurl_pattern = 'http://img.mmjpg.com/small/.*?.jpg'
        picid_pattern = 'http://img.mmjpg.com/small/(.*?).jpg'

        # import random
        # random_index = random.randint(0, len(user_agent_list) - 1)
        # random_agent = user_agent_list[random_index]
        #
        # headers = {"Referer": "http://www.mmjpg.com/",
        #            "User-Agent": random_agent
        #            }
        # opener = urllib.request.build_opener()
        # opener.addheaders = [headers]
        # urllib.request.install_opener(opener)

        picurl_list = re.findall(picurl_pattern, str(response.body))
        picid_list = re.findall(picid_pattern, str(response.body))
        for i in range(0, len(picurl_list)):
            item['picurl'] = picurl_list[i]
            item['picid'] = picid_list[i]
            yield item
