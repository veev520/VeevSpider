#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Veev'

import requests
from bs4 import BeautifulSoup
from lxml import etree
from club.veev.veevspider.base import log, header_helper, proxy_helper

site = 'https://m.lianjia.com'
# site = 'https://www.lianjia.com'
url = 'https://m.lianjia.com/city/'
city_list = list()


def get_city():
    global city_list
    proxy = proxy_helper.get(site)
    if not proxy:
        return
    r = requests.get(url=url, headers=header_helper.mobile(), proxies=proxy, timeout=20)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, "lxml")
        log.i(soup)
        li_item = soup.find_all('li', {'class': 'li_item'})
        log.i(li_item)
        for li in li_item:
            a = li.a
            city = dict()
            city['url'] = a['href']
            city['city'] = a.text
            city_list.append(city)
    log.i(city_list)
    pass


def save_city_to_csv():
    import csv
    with open('city' + '.csv', 'a', encoding='utf-8') as csvfile:
        fieldnames = ['url', 'city']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        for d in city_list:
            writer.writerow(d)
        log.i('数据写入中...')


if __name__ == '__main__':
    # get_city()
    # save_city_to_csv()
    log.i(0)
