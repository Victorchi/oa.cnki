# coding=utf-8
import pymysql
import re
import codecs
import time
import datetime
import os


from abc import abstractmethod


class BaseSQL(object):
    """
    关系型数据库操作类： 抽象类

    """
    def __init__(self, server, port, username, password, database, charset="utf8"):
        if server is None or len(server) == 0:
            raise ValueError("args[Server] must not be empty.")
        if username is None or len(username) == 0:
            raise ValueError("args[username] must not be empty.")
        if password is None or len(password) == 0:
            raise ValueError("args[password] must not be empty.")
        if port is None:
            raise ValueError("args[port] must not be empty.")
        if not isinstance(port, int):
            raise ValueError("args[port] type must be an integer value.")
        self.server = server
        self.port = port
        self.username = username
        self.password = password
        self.database = database
        self.charset = charset

    @abstractmethod
    def _get_connect(self):
        pass

    def find_all(self, sql):
        """
        执行查询语句
        返回的是一个包含tuple的list，list的元素是记录行，tuple的元素是每行记录的字段
        """
        conn = self._get_connect()
        cur = conn.cursor()
        cur.execute(sql)
        resList = cur.fetchall()
        cur.close()
        # 查询完毕后必须关闭连接
        conn.close()
        return resList

    def exec_nonquery(self, sql):
        """
        执行非查询语句

        调用示例：
            cur = self.__GetConnect()
            cur.execute(sql)
            self.conn.commit()
            self.conn.close()
        """
        conn = self._get_connect()
        cur = conn.cursor()
        cur.execute(sql)
        cur.close()
        conn.commit()
        conn.close()

class MYSQL(BaseSQL):
    """
    MYSQL数据库操作类：对pymysql的简单封装
    """
    def __init__(self, server, username, password, database, charset="utf8", port=3306):
        super().__init__(server=server
                         , port=port
                         , username=username
                         , password=password
                         , database=database
                         , charset=charset)

    def _get_connect(self):
        """
        得到连接信息
        返回: conn.cursor()
        """
        if not self.server:
            raise(NameError, "没有设置数据库信息")
        return pymysql.connect(
            host=self.server,
            user=self.username,
            password=self.password,
            database=self.database,
            charset=self.charset,
            port=self.port)



def Rec(txt_path, limit):
    mssql = MYSQL("localhost", "root", "123321", "spiders")
    a1 = time.time()
    sql = 'Select url,title from contents WHERE vendor ="wanfang" and isRec = 1 limit {},2500'.format(limit)
    contents = mssql.find_all(sql)
    if len(contents) < 0:
        return True
    a2 = time.time()
    # print('数据查询用时', a2 - a1)
    with open(txt_path, 'a+', encoding='utf-8') as f:
        count = 0
        _list = []
        for content in contents:
            f.write('\n<REC>')
            item = {}
            item['ABS_LINK'] = content[0]
            item['TITLE'] = content[1]
            item['YEAR'] = year(content[0])
            for key, value in item.items():
                f.write('\n<{key}>={value}'.format(key=key, value=value))
            count += 1
            sql = "UPDATE contents SET isRec = 0 where url='{}'".format(content[0])
            _list.append(sql)
        a3 = time.time()
        # print('写入2000条数据到文件用时', a3 - a2)
        mssql.exec_nonquery(';'.join(_list))
        a4 = time.time()
        # print('已有{}条插入成功:插入数据库用时'.format(count), a4 - a3)


# def Rec(txt_path,limit):
#     sql = 'Select url,title from contents WHERE vendor ="wanfang" and isRec = 0 limit {},5000'.format(limit)
#     contents = OperationMysql().find_all(sql)
#     print('共计有{}条数据'.format(len(contents)))
#     if len(contents)<1:
#         return True
#     count = 0
#     f = codecs.open(txt_path, 'a', 'utf-8')
#     for content in contents:

#         f.write('\n<REC>')
#         item = {}
#         item['ABS_LINK'] = content[0]
#         item['TITLE'] = content[1]
#         item['YEAR'] = year(content[0])
#         for key,value in item.items():
#             f.write('\n<{key}>={value}'.format(key = key,value=value))
#         count +=1
#     f.close()
#     print('已有{}条插入成功'.format(count))
def year(url):
    year = re.sub('.+perio&id=', '', url)
    year = re.sub('[A-Za-z]|\W', '', year)
    try:
        # issue = re.sub('^\d{4}', '', year)
        year = re.findall('^\d{4}', year)[0]
    except:
        # issue = 0
        year = 0
    if 1850 < int(year) < 2100:
        year = year
    else:
        year = ''
    return str(year)


def creat_file():
    '''返回一个小于500M的文件,或者是创建一个新的文件'''

    dir = 'D:\\新建文件夹\\'
    _list = os.listdir(dir)
    _list.remove('rec_wanfang.py')
    count = 0
    file_size = []
    for i in _list:
        file_size.append(os.path.getsize(i))
    for i in _list:
        count += 1
        if os.path.getsize(i) > 500000000:
            continue
        elif os.path.getsize(i) < 500000000:
            return dir + i
    try:
        if min(file_size) > 500000000:
            name = 'wanfang{}.txt'.format(len(_list) + 1)
            return dir + name

    except ValueError:
        name =dir+ 'wanfang1.txt'
        return name
def start():
    count = 1
    i = 0
    name =creat_file()
    if Rec(name, i):
        return


def run():
    # print('任务开始')
    a = time.time()
    start()
    b = time.time()
    print('2500条数据共计耗时{}'.format(b - a))
    # time.sleep(1)


if __name__ == '__main__':
    a = time.time()
    for i in range(20000):
        run()
    b = time.time()
    print('共计耗时{}'.format(b - a))