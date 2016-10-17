# -*- coding: utf-8 -*-

# Need chromedriver & selenium to be installed!!

import scrapy
import pickle
import sys
from selenium import webdriver
import time


def user_select_category(list, layer):
    print("-------------------------------------------")
    print('Please select from the %dth-layer category.' % layer)
    for i in range(len(list)):
        try:
            sys.stdout.write(
                "%d %-10s\t" % (i, list[i].find_element_by_xpath('./a/span').text)
            )
        except:
            break
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

    def __init__(self):
        self.chrome = webdriver.Chrome()
        self.chrome.get(self.start_urls[0])

    def __del__(self):
        self.chrome.close()
        print("Chrome window closed.")

    def parse(self, response):
        self.chrome.get(self.start_urls[0])
        category_url = self.chrome.find_element_by_xpath(
            '//span[@class="schfunc"]/a[2]' # xpath is 1-based
        ).get_attribute('href')
        print("found category_url: %s" % category_url)
        res = self.select_category(category_url, 0)
        # self.chrome.close()
        return res

    def select_category(self, abs_url, layer):
        print("++++++++++++ layer: %d" % layer)
        self.chrome.get(abs_url)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(abs_url)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        table_ele = self.chrome.find_elements_by_xpath(
            '(//table[@class="brwlv_table"])[' + str(layer + 1) + ']'
            + '/tbody/tr/td[@class="brwlv_item_td"]'
        )
        print(table_ele)
        if len(table_ele) == 0:
            print("# no requested list.")
            return None

        # href = table_ele.find_elements_by_xpath('./a').get_attribute('href')
        
        # category = table_ele.find_elements_by_xpath('./a/span').text

        selected = user_select_category(table_ele, layer)
        if selected < 0 or selected >= len(table_ele):
            print("Error input: %d" % selected)
            return None # Should close crawler immediately.

        selected_href = table_ele[selected].find_element_by_xpath(
            './a'
        ).get_attribute('href')

        # reset layer
        if layer < 2:
            res = self.select_category(selected_href,
                                       layer + 1)
            return res
        else: # layer = 2
            res = self.parse_pages(selected_href)
            return res

    def parse_pages(self, abs_url):
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(abs_url)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        self.chrome.get(abs_url)
        
        url_list = []

        # parse papers in multiple pages.
        while True:
            # Wait until 5 sec or page loaded.
            # self.chrome.manage().timeouts().pageLoadTimeout(5, TimeUnit.SECONDS);
            article = self.chrome.find_elements_by_xpath(
                '//table[@class="tableoutsimplefmt2"]'
                '/tbody/tr/td/a[@class="slink"]'
            )
            print(article)
            for a in article:
                link = a.get_attribute('href')
                # title = a.find_element_by_xpath('span').text
                # print("$$$ title %s" % title)
                # a.click()
                # res = self.parse_article(link, title)
                # yield res
                url_list.append(link)
            
            # click next page button
            try:
                self.chrome.find_element_by_xpath(
                    '//input[@name="gonext"]'
                ).click()
            except:
                print("%%%%%%%% No page left. %%%%%%%%%%")
                break

        time.sleep(1)
        # starts parsing pages
        for url in url_list:
            res = self.parse_article(url)
            yield res

    def parse_article(self, abs_url):
        self.chrome.get(abs_url)
        print(abs_url)
        # get titles
        ch_title = self.chrome.find_element_by_xpath(
            '//table[@id="format0_disparea"]/tbody/tr[4]/td'
        ).text
        print(ch_title)

        en_title = self.chrome.find_element_by_xpath(
            '//table[@id="format0_disparea"]/tbody/tr[5]/td'
        ).text
        print(en_title)

        # parse single article.
        # chinese = self.chrome.find_element_by_xpath(
            # '(//td[@class="stdncl2"])[1]/div'
        # ).get_attribute('innerHTML')

        english = self.chrome.find_element_by_xpath(
            '(//td[@class="stdncl2"])[2]/div'
        ).get_attribute('innerHTML')

        keyword = self.chrome.find_element_by_xpath(
            '//table[@id="format0_disparea"]/tbody/tr/td[preceding-sibling::th[contains(.,"外文關鍵詞")]]'
        ).text

        print(">>>>>>> " + keyword)

        # self.chrome.back()

        return {"post": {
            "English_title": en_title,
            "English_abstract": english,
            "keyword": keyword
        }}


