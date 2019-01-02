# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     common
   Description :   放置一些常用的函数
   Author :       wsm
   date：          19-1-2
-------------------------------------------------
   Change Activity:
                   19-1-2:
-------------------------------------------------
"""
__author__ = 'wsm'
import hashlib

def get_md5(url):
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()

if __name__ == "__main__":
    print(get_md5("https://baidu.com".encode("utf-8")))
