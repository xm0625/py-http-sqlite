# coding=utf-8

# 解决py2.7中文出现write错误的问题
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
# 解决py2.7中文出现write错误的问题 #
import urllib2
import urllib
import json


_url = "http://127.0.0.1:50001/execute"


class ExecuteSqlMethod(object):
    execute = "execute"
    executemany = "executemany"
    executescript = "executescript"


class ExecuteSqlResultMethod(object):
    fetchall = "fetchall"
    rowcount = "rowcount"


def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


def execute_batch(execute_list, result_method):
    task_obj = {
        "execute_list": execute_list,
        "result_method": result_method
    }
    req = urllib2.Request(_url, urllib.urlencode({"task_obj": json.dumps(task_obj, ensure_ascii=False)}))
    response = urllib2.urlopen(req)
    content = response.read()
    content_obj = byteify(json.loads(content))
    return content_obj["result"]


def execute_sql(method, sql, param, result_method):
    return execute_batch([{"method": method, "sql": sql, "param": param}], result_method)

