# coding=utf-8

# 解决py2.7中文出现write错误的问题
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
# 解决py2.7中文出现write错误的问题 #

# 从wsgiref模块导入:
from wsgiref.simple_server import make_server
import urlparse
import json
import sqlite3

connection = None
cursor = None


class CommonException(Exception):
    code = "0"
    message = "system busy"
    """docstring for CommonException"""

    def __init__(self, code, message="system busy"):
        super(CommonException, self).__init__()
        if code:
            self.code = code
        if message:
            self.message = message


def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


def execute(request):
    if "task_obj" not in request.keys():
        raise CommonException("-1", "缺少task_obj")
    task_obj_string = request["task_obj"]
    task_obj = byteify(json.loads(task_obj_string))
    execute_list = task_obj["execute_list"]
    execute_result_method = task_obj["result_method"]
    result = ""
    try:
        for execute_item in execute_list:
            execute_item_method = execute_item["method"]
            execute_item_sql = execute_item["sql"]
            execute_item_param = execute_item["param"]
            if execute_item_method == "execute":
                cursor.execute(execute_item_sql, tuple(execute_item_param))
            if execute_item_method == "executemany":
                cursor.executemany(execute_item_sql, execute_item_param)
            if execute_item_method == "executescript":
                cursor.executescript(execute_item_sql)
        connection.commit()
        if execute_result_method == "fetchall":
            result = cursor.fetchall()
        if execute_result_method == "rowcount":
            result = cursor.rowcount
    except Exception as e:
        connection.rollback()
        result = "error," + str(e.message)
    if isinstance(result, str) and result.startswith("error"):
        raise CommonException("-2", "数据库错误," + result)
    return result


def app(environ, start_response):
    request_method = environ["REQUEST_METHOD"]  # GET
    path_info = environ["PATH_INFO"]  # /hi/name/index.action
    query_string = environ["QUERY_STRING"]  # ?后面的东西
    remote_address = environ["REMOTE_ADDR"]  # 访问者ip
    print "request_method:" + request_method
    print "path_info:" + path_info
    print "remote_address:" + remote_address

    if request_method == "GET":
        request = urlparse.parse_qs(query_string)
    else:
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        except (ValueError):
            request_body_size = 0
        request_body = environ['wsgi.input'].read(request_body_size)
        request = urlparse.parse_qs(request_body)
    for (d, x) in request.items():
        if isinstance(x, list) and len(x) == 1:
            request[d] = x[0]
    for (d, x) in request.items():
        print "key:" + d + ",value:" + str(x)

    if path_info == "/":
        response_string = ""
        response_code = "200 OK"
        response_header = [('Content-type', 'text/html'), ('Access-Control-Allow-Origin', '*'),
                           ('Access-Control-Allow-Credentials', 'true'),
                           ('Access-Control-Allow-Methods', 'GET, POST, OPTIONS'), ('Access-Control-Allow-Headers',
                                                                                    'DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type')]
        try:
            fetch_result = "ok"
            response_data = {"code": "0", "message": "success", "result": fetch_result}
            response_string = json.dumps(response_data, ensure_ascii=False)
        except CommonException as ce:
            response_string = '{"code":"' + ce.code + '","message":"' + ce.message + '"}'
        except ValueError:
            response_string = '{"code":"-1","message":"system busy"}'
    elif path_info == "/execute":
        response_string = ""
        response_code = "200 OK"
        response_header = [('Content-type', 'text/html'), ('Access-Control-Allow-Origin', '*'),
                           ('Access-Control-Allow-Credentials', 'true'),
                           ('Access-Control-Allow-Methods', 'GET, POST, OPTIONS'), ('Access-Control-Allow-Headers',
                                                                                    'DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type')]
        try:
            result = execute(request)
            response_data = {"code": "0", "message": "success", "result": result}
            response_string = json.dumps(response_data, ensure_ascii=False)
        except CommonException as ce:
            response_string = '{"code":"' + ce.code + '","message":"' + ce.message + '"}'
        except ValueError:
            response_string = '{"code":"-1","message":"system busy"}'
    else:
        response_string = "404 NOT FOUND"
        response_code = "404 NOT FOUND"
        response_header = [('Content-type', 'text/html'), ('Access-Control-Allow-Origin', '*'),
                           ('Access-Control-Allow-Credentials', 'true'),
                           ('Access-Control-Allow-Methods', 'GET, POST, OPTIONS'), ('Access-Control-Allow-Headers',
                                                                                    'DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type')]
    start_response(response_code, response_header)
    return [response_string]


def init():
    global connection
    global cursor
    connection = sqlite3.connect("db.sqlite")
    connection.text_factory = str
    cursor = connection.cursor()
    cursor.executescript("""
            DROP TABLE IF EXISTS person;
            DROP TABLE IF EXISTS book;

            CREATE TABLE person(
                firstname,
                lastname,
                age
            );

            CREATE TABLE book(
                title,
                author,
                published
            );

            INSERT INTO book(title, author, published)
            VALUES (
                'Dirk Gently''s Holistic Detective Agency',
                'Douglas Adams',
                1987
            );
        """)


def run():
    init()
    httpd = make_server('127.0.0.1', 50001, app)
    print "Serving HTTP on port 50001..."
    # 开始监听HTTP请求:
    httpd.serve_forever()


if __name__ == "__main__":
    run()
