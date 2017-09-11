# -*- coding: utf-8 -*-
"""
代理帮助模块
"""

import threading

import pymysql
import requests
from bs4 import BeautifulSoup
from lxml import etree
import log
import time

from base import header_helper as header

test_url = ['https://m.lianjia.com']


def get(site='default'):
    d = _ProxyStorage()
    proxy = d.get(site)
    d.close()
    if not proxy:
        return None
    p = {"http": "http://{}:{}".format(proxy[3], proxy[4]),
         "https": "https://{}:{}".format(proxy[3], proxy[4])}
    return p


class _ProxyStorage:
    def __init__(self, site='default'):
        self.__site = site
        self.__reset()
        pass

    def put(self, ip, port, site):
        self.__insert_item(site if site else self.__site, ip, port)
        pass

    def get(self, site):
        # SQL 查询语句
        result = self.__query_item(site if site else self.__site)
        if result:
            self.__delete_item(result[0][0])
            return result[0]
        return None

    def __reset(self):
        self.__db = pymysql.connect("127.0.0.1", "root", "123456", "py_test")
        self.__cursor = self.__db.cursor()
        pass

    def __query_item(self, site):
        # SQL 查询语句
        sql = "SELECT * FROM proxy WHERE site = '%s'" % (site)
        results = []
        try:
            # 执行SQL语句
            self.__cursor.execute(sql)
            # 获取所有记录列表
            results = self.__cursor.fetchall()
        except Exception as e:
            log.i('查询数据异常', e)
        finally:
            return results

    def __insert_item(self, site, ip, port):
        # SQL 查询语句
        proxy = ip + ':' + port
        sql = "INSERT INTO proxy(site, proxy, ip, port) VALUES ('%s', '%s', '%s', '%s')" \
              % (site, proxy, ip, port)
        try:
            # 执行SQL语句
            self.__cursor.execute(sql)
            # 提交到数据库执行
            self.__db.commit()
        except Exception as e:
            log.i('插入数据异常', e)
            self.__db.rollback()

    def __delete_item(self, id):
        # SQL 查询语句
        sql = "DELETE FROM proxy WHERE id='%s'" % (id)
        try:
            # 执行SQL语句
            self.__cursor.execute(sql)
            self.__db.commit()
        except Exception as e:
            log.i('删除数据异常', e)
            self.__db.rollback()

    def __close(self):
        if not self.__db._closed:
            self.__db.close()
        pass

    def close(self):
        self.__close()

    pass


class ProxySpider:
    def __init__(self):
        # 存储单元
        global _ps
        # 锁 - 存储
        global _lock_storage
        global _quene_proxy
        _ps = _ProxyStorage()
        _lock_storage = threading.Lock()
        _quene_proxy = []
        pass

    def start(self):
        thread_list = []
        log.i('==========  开始爬  ==========')
        # 爬
        thread_list.append(threading.Thread(target=self.get_xi_ci()))
        thread_list.append(threading.Thread(target=self.get_data_5u()))
        thread_list.append(threading.Thread(target=self.get_ip_181()))

        for t in thread_list:
            t.start()
        for t in thread_list:
            t.join()
        # 校验
        log.i('==========  准备校验  ==========')
        self.__check()
        pass

    def get_xi_ci(self):
        """
        西刺代理
        """
        url_list = ('http://www.xicidaili.com/nn',  # 高匿
                    'http://www.xicidaili.com/nt',  # 透明
                    )
        __count = 0
        for url in url_list:
            try:
                r = requests.get(url=url, headers=header.pc())
                if r.status_code == 200:
                    soup = BeautifulSoup(r.text, "lxml")
                    odd = soup.find_all('tr', {'class': 'odd'})
                    for o in odd:
                        ts = o.find_all('td')
                        proxy = (ts[1].text, ts[2].text)
                        _quene_proxy.append(proxy)
                        __count += 1
            except Exception as e:
                pass
        log.i('-- 西刺爬取完成, 共计 %d 条 --' % __count)
        pass

    def get_data_5u(self):
        """
        无忧代理
        """
        url_list = ('http://www.data5u.com/free/gngn/index.shtml',  # 高匿
                    'http://www.data5u.com/free/gnpt/index.shtml',  # 普通
                    )
        __count = 0
        for url in url_list:
            try:
                r = requests.get(url=url, headers=header.pc())
                log.i('5u', r.status_code)
                if r.status_code == 200:
                    tree = etree.HTML(r.text)
                    ul_list = tree.xpath('//ul[@class="l2"]')
                    for ul in ul_list:
                        proxy = (ul.xpath('.//li/text()')[0], ul.xpath('.//li/text()')[1])
                        _quene_proxy.append(proxy)
                        __count += 1
            except Exception as e:
                pass
        log.i('-- 无忧爬取完成, 共计 %d 条 --' % __count)

    def get_ip_181(self):
        """
        ip181
        """
        url = 'http://www.ip181.com/'
        __count = 0
        try:
            r = requests.get(url=url, headers=header.pc())
            log.i('181', r.status_code)
            if r.status_code == 200:
                tree = etree.HTML(r.text)
                tr_list = tree.xpath('//tr')[1:]
                for tr in tr_list:
                    proxy = (tr.xpath('./td/text()')[0], tr.xpath('./td/text()')[1])
                    _quene_proxy.append(proxy)
                    __count += 1
        except Exception as e:
            pass
        log.i('-- ip181爬取完成, 共计 %d 条 --' % __count)

    def __check(self):
        while _quene_proxy:
            while len(threading.enumerate()) < 128:
                _Checker(_quene_proxy.pop(0)).start()
        log.i('==========  校验完毕  ==========')
        pass

    pass


class _Checker(threading.Thread):
    """
    代理校验类 
    """

    def __init__(self, proxy):
        threading.Thread.__init__(self)
        self.p = proxy

    def run(self):
        try:
            p = {"http": "http://{}:{}".format(self.p[0], self.p[1]),
                 "https": "https://{}:{}".format(self.p[0], self.p[1])}
            for url in test_url:
                r = requests.get(url=url,
                                 headers=header.pc(),
                                 timeout=20,
                                 proxies=p)
                if r.status_code == 200:
                    log.i('代理测试通过: ', self.p)
                    # 获取锁:
                    _lock_storage.acquire()
                    try:
                        _ps.put(self.p[0], self.p[1], url)
                        pass
                    finally:
                        # 释放锁:
                        _lock_storage.release()
        except BaseException as e:
            log.i('代理测试失败, 异常 ---> ', self.p, e)


if __name__ == '__main__':
    spider = ProxySpider()
    # spider.start()
    log.i(49)
    pass