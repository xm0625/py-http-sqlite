# coding=utf-8

# 解决py2.7中文出现write错误的问题
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
# 解决py2.7中文出现write错误的问题 #

import sqlite_server_helper as helper
import time

if __name__ == "__main__":
    url = "http://127.0.0.1:50001/execute"

    start = time.time()
    for i in xrange(20):
        content = helper.execute_batch(
            [{"method": helper.ExecuteSqlMethod.execute, "sql": "select * from book;", "param": []}],
            helper.ExecuteSqlResultMethod.fetchall)
        # print(content)
    print("多次请求,查询20次,耗时:" + str(time.time() - start) + "s")

    start = time.time()
    for i in xrange(20):
        content = helper.execute_batch(
            [{"method": helper.ExecuteSqlMethod.execute,
                 "sql": "insert into book(title,author,published) VALUES(?,?,?);",
                 "param": [str(i), "xm", "xm"]}],
            helper.ExecuteSqlResultMethod.rowcount)
        # print(content)
    print("多次请求,更新20条,耗时:" + str(time.time() - start) + "s")

    start = time.time()
    param = []
    for i in xrange(20):
        param += [[str(i), "许鸣", "xm"]]
    content = helper.execute_batch(
        [{"method": helper.ExecuteSqlMethod.executemany,
             "sql": "insert into book(title,author,published) VALUES(?,?,?);",
             "param": param}],
        helper.ExecuteSqlResultMethod.rowcount
    )
    # print(content)
    print("单次请求,批量更新20条,耗时:" + str(time.time() - start) + "s")

    start = time.time()
    execute_list = []
    for i in xrange(20):
        execute_list += [{"method": helper.ExecuteSqlMethod.execute,
                          "sql": "insert into book(title,author,published) VALUES(?,?,?);",
                          "param": [str(i), "xm", "xm"]}]
    content = helper.execute_batch(execute_list, helper.ExecuteSqlResultMethod.rowcount)
    # print(content)
    print("单次请求,批量执行20条更新,耗时:" + str(time.time() - start) + "s")
