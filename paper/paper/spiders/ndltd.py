# -*- coding: utf-8 -*-
import scrapy
import pickle
import sys

def user_select_category(list, layer):
    print("-------------------------------------------")
    print('Please select from the %dth-layer category.' % layer)
    for i in range(len(list)):
        sys.stdout.write("%d %-10s\t" % (i, list[i]))
        if (i + 1) % 4 == 0:
            sys.stdout.write('\n')
    sys.stdout.write('\n')

    selected = int(input (" >>> (Enter number.) "))
    print("-------------------------------------------")
    return selected


class NdltdSpider(scrapy.Spider):
    name = "ndltd"
    allowed_domains = ["ndltd.ncl.edu.tw"]
    start_urls = ( 
        'http://ndltd.ncl.edu.tw/cgi-bin/gs32/gsweb.cgi/login?o=dwebmge', 
    )
    rooturl = 'http://ndltd.ncl.edu.tw'

    def parse(self, response):
        category_url = response.css(
            'a[href*=browselevel]::attr(href)'
        ).extract()[0]
        print("found category_url: %s" % category_url)
        req = scrapy.Request(self.rooturl + category_url,
                             callback=self.select_category)
        req.meta['layer'] = 0
        return req

    def select_category(self, response):
        layer = int(response.meta['layer'])
        print("++++++++++++ layer: %d" % layer)
        table_ele = response \
            .xpath('//table[@class="brwlv_table"]')[layer] \
            .xpath('./tr/td[@class="brwlv_item_td"]')

        href = table_ele.xpath('./a/@href').extract()
        
        category = table_ele.xpath('./a/span/text()').extract()

        selected = user_select_category(category, layer)
        if selected < 0 or selected >= len(category):
            print("Error input: %d" % selected)
            return {} # Should close crawler immediately.

        # reset layer
        if layer < 2:
            req = scrapy.Request(self.rooturl + href[selected],
                                 callback=self.select_category)
            req.meta['layer'] = layer+1
            return req
        else: # layer = 2
            return scrapy.Request(self.rooturl + href[selected],
                                  callback=self.parse_pages)

    def parse_pages(self, response):
        # parse papers in multiple pages.
        article = response.xpath(
            '//table[@class="tableoutsimplefmt2"]/tr/td/a[@class="slink"]'
        )
        for idx in range(len(article)):
            link = article[idx].xpath('@href').extract_first()
            title = article[idx].xpath('span').extract_first()
            req = scrapy.Request(self.rooturl + link,
                                 callback=self.parse_article)
            req.meta['title'] = title
            yield req

    def parse_article(self, response):
        # parse single article.
        chinese = response.xpath(
            '//td[@class="stdncl2"]/div/text()'
        )[0].extract()
        english = response.xpath(
            '//td[@class="stdncl2"]/div/text()'
        )[1].extract()

        return {"post": {
            "title": response.meta['title'],
            "Chinese": chinese,
            "English": english
        }}


