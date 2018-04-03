# -*- coding: utf-8 -*-
import scrapy
import re
import urllib.request

from picspider.items import PicspiderItem


class PicSpider(scrapy.Spider):
    name = 'pic'
    allowed_domains = ['mmjpg.com']
    start_urls = ('http://www.mmjpg.com/',)

    def parse(self, response):
        item = PicspiderItem()

        picurl_pattern = 'http://img.mmjpg.com/small/.*?.jpg'
        picid_pattern = 'http://img.mmjpg.com/small/(.*?).jpg'

        headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0",
                   "Referer": "http://www.mmjpg.com/"}
        opener = urllib.request.build_opener()
        opener.addheaders = [headers]
        urllib.request.install_opener(opener)

        picurl_list = re.findall(picurl_pattern, str(response.body))
        picid_list = re.findall(picid_pattern, str(response.body))
        for i in range(0, len(picurl_list)):
            item['picurl'] = picurl_list[i]
            item['picid'] = picid_list[i]
            yield item
