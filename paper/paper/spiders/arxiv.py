# -*- coding: utf-8 -*-
import scrapy
import math


class ArxivSpider(scrapy.Spider):
    name = "arxiv"
    allowed_domains = ["arxiv.org"]
    start_urls = ()

    def start_requests(self):
        category = input(">>> Category (can be found in arxiv.cat): ")

        start_str = input(">>> Start from (def 0): ")
        start = 0
        if len(start_str) > 0:
            start = int(start_str)

        max_str = input(">>> Max index (def 20000): ")
        max_id = 20000
        if len(max_str) > 0:
            max_id = int(max_str)

        print("parsing range: %d - %d" % (start, max_id))

        step_n = 100
        count = start
        for id in range(math.floor((max_id - start + 1) / step_n) + 1):
            limit = min(max_id - count + 1, step_n)
            url = "http://export.arxiv.org/api/query?search_query=cat:{}" \
                  "&start={}&max_results={}".format(
                    category, str(count), str(limit)
                  )
            count += step_n
            
            res = scrapy.Request(url, callback=self.parsexml)
            if res is None:
                break
            yield res

    def parsexml(self, response):
        response.selector.register_namespace('d', 'http://www.w3.org/2005/Atom')
        list = response.xpath('//d:entry')
        if len(list) == 0:
            print("Empty list...")
            return None
        for obj in list:
            yield {"post": {
                "title": obj.xpath('./d:title/text()')[0].extract(),
                "abstract": obj.xpath('./d:summary/text()')[0].extract()
            }}

