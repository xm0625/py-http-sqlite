py-http-sqlite
===
  python下的多进程(分布式进程)同时读写sqlite的demo(单线程http server版)  
  
原理简介
----
  没啥好解释的,单线程http server天然保证串行访问数据库,不会存在并发问题.  
  一个请求在未处理完成前,所有的其他的sqlite操作请求(http请求)都被阻塞
  
特点
---
  1.多进程访问sqlite  
  2.多个语句可以在一次事务中执行  
  3.是py-multiprogress-sqlite的优化版,缩短了进程间(server与client)数据交互的时间,将queue,pipe改为http
  
环境需求
---
  Python2.6+(Python3需要自行改造)  
  
如何运行
---
  1.下载项目源码  
  2.进入项目源码文件夹  
  3.执行 python sqlite_server.py
  3.执行 python client-demo.py  
  
License
---
  MIT license.
![img](data:image/gif;base64,R0lGODlhEAAOALMAAOazToeHh0tLS/7LZv/0jvb29t/f3//Ub//ge8WSLf/rhf/3kdbW1mxsbP//mf///yH5BAAAAAAALAAAAAAQAA4AAARe8L1Ekyky67QZ1hLnjM5UUde0ECwLJoExKcppV0aCcGCmTIHEIUEqjgaORCMxIC6e0CcguWw6aFjsVMkkIr7g77ZKPJjPZqIyd7sJAgVGoEGv2xsBxqNgYPj/gAwXEQA7)
