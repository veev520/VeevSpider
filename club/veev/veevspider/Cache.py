import pymysql


class Cache:
    def __init__(self, room='cache'):
        self.__room = room
        self.__reset()
        pass

    def set(self, k, v):
        result = self.__query_item(k)
        if len(result) != 0:
            id = result[0][0]
            self.__update_item(id, v)
        else:
            self.__insert_item(k, v)
        pass

    def get(self, k):
        # SQL 查询语句
        result = self.__query_item(k)
        if result:
            return result[0][3]
        return None

    def remove(self, k):
        result = self.__query_item(k)
        if result:
            id = result[0][0]
            self.__delete_item(id)
        pass

    def clear(self, k):
        pass

    def has_key(self, k):
        result = self.__query_item(k)
        return True if len(result) != 0 else False

    def __reset(self):
        self.__db = pymysql.connect("127.0.0.1", "root", "123456", "py_test")
        self.__cursor = self.__db.cursor()
        pass

    def __query_item(self, k):
        # SQL 查询语句
        sql = "SELECT * FROM kv WHERE room = '%s' and k = '%s'" % (self.__room, k)
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

    def __insert_item(self, k, v):
        # SQL 查询语句
        sql = "INSERT INTO kv(room, k, v) VALUES ('%s', '%s', '%s')" % (self.__room, k, v)
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

    def __update_item(self, id, v):
        # SQL 查询语句
        sql = "UPDATE kv SET v='%s' WHERE id='%s'" % (v, id)
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

    def __delete_item(self, id):
        # SQL 查询语句
        sql = "DELETE FROM kv WHERE id='%s'" % (id)
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

    pass


if __name__ == '__main__':
    cache = Cache('d')
    print(cache.get('k1'))

