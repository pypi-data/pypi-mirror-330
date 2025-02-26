# -*- coding: utf-8 -*-
# @Time    : 2024/12/24 16:50
# @Author  : xuwei
# @FileName: es_op.py
# @Software: PyCharm


from elasticsearch import AsyncElasticsearch
from .dotenv_config import config

"""
Elasticsearch DSL 是一个高级库，旨在帮助编写和运行针对 Elasticsearch 的查询。它建立在官方低级客户端 (elasticsearch) 之上，主要用于orm操作。

简单的body查询用elasticsearch库就足够了

该代码只简单封装了es连接建立，通过编写body实现异步查询
"""


class EsOpAsync:
    def __init__(self, label, alias="default", timeout=20, config_map=None):
        self.__alias = alias
        self.__config_map = config_map
        self.__label = label
        self.__timeout = timeout

        if self.__config_map:
            hosts = self.__config_map['host'].split(",")  # 英文逗号分割
            user = self.__config_map.get('user', '')
            password = self.__config_map.get('pass', '')
        else:
            hosts = config(self.__label, 'host').split(",")  # 英文逗号分割
            user = config(self.__label, 'user', '')
            password = config(self.__label, 'pass', '')

        self.client = AsyncElasticsearch(hosts=hosts, http_auth=(user, password), timeout=self.__timeout)

    async def query(self, index: str, body: dict, **kwargs):
        """
        :param index:
        :param body: body = {"query": {"match": {"title": title}}, "from": 0, "size": 1}
        :return:
        """
        res = await self.client.search(index=index, body=body, **kwargs)
        response = res.body
        return response

    async def close(self):
        await self.client.close()
