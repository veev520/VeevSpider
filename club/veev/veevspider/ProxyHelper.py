import pymysql


def get(site='default'):
    d = ProxyStorage()
    proxy = d.get(site)
    d.close()
    if not proxy:
        return None
    p = {"http": "http://{}:{}".format(proxy[3], proxy[4]),
         "https": "https://{}:{}".format(proxy[3], proxy[4])}
    return p


class ProxyStorage:
    def __init__(self, site='default'):
        self.__site = site
        self.__reset()
        pass

    def put(self, ip, port, site):
        self.__insert_item(self.__site if site else site, ip, port)
        pass

    def get(self, site):
        # SQL 查询语句
        result = self.__query_item(self.__site if site else site)
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
            # self.__reset()
            # 执行SQL语句
            self.__cursor.execute(sql)
            # 获取所有记录列表
            results = self.__cursor.fetchall()
        except Exception as e:
            print(e)
        finally:
            # self.__close()
            return results

    def __insert_item(self, site, ip, port):
        # SQL 查询语句
        proxy = ip + ':' + port
        sql = "INSERT INTO proxy(site, proxy, ip, port) VALUES ('%s', '%s', '%s', '%s')" \
              % (site, proxy, ip, port)
        print(sql)
        try:
            # self.__reset()
            # 执行SQL语句
            self.__cursor.execute(sql)
            # 提交到数据库执行
            self.__db.commit()
        except Exception as e:
            print(e)
            self.__db.rollback()
        # finally:
        #     self.__close()

    def __delete_item(self, id):
        # SQL 查询语句
        sql = "DELETE FROM proxy WHERE id='%s'" % (id)
        try:
            # self.__reset()
            # 执行SQL语句
            self.__cursor.execute(sql)
            self.__db.commit()
        except Exception as e:
            print(e)
            self.__db.rollback()
        # finally:
        #     self.__close()

    def __close(self):
        if not self.__db._closed:
            self.__db.close()
        pass

    def close(self):
        self.__close()

    pass


class ProxySpider:
    def __init__(self):
        pass
    pass


if __name__ == '__main__':
    # c = Cache('https://nj.lianjia.com')
    print(get('https://nj.lianjia.com'))
