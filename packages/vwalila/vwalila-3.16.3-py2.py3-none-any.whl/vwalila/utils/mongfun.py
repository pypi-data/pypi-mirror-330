# -*- coding: UTF-8 -*-

from pymongo import MongoClient
from pymongo import ReadPreference

READ_SLAVE = ReadPreference.SECONDARY_PREFERRED
READ_PRIMARY = ReadPreference.PRIMARY


class MongodbClient(object):
    def __init__(self, url, connect_timeout_ms=30000):
        """
        不要提前初始化Client，见下文链接
        "MongoClient opened before fork. Create MongoClient only "
        # http://api.mongodb.org/python/current/faq.html#is-pymongo-fork-safe
        :param url:
        """
        self.mongodb_url = url
        self.mongodb_client = None
        self.db_mapping = {}
        self.connect_timeout_ms = connect_timeout_ms

    def get_mongodb_conn(self, url, connect_timeout_ms=30000):
        """
        One or more mongos instances. The mongos instances are the routers for the
        cluster. Typically, deployments
    have one mongos instance on each application server.
        You may also deploy a group of mongos instances and use a proxy/load
        balancer between the application and the mongos.
    In these deployments, you must configure the load balancer for client affinity
    so that every connection from a
    single client reaches the same mongos.
        Because cursors and other resources are specific to an single mongos
        instance, each client must interact with
    only one mongos instance.
        :return:
        """
        return MongoClient(url, serverSelectionTimeoutMS=connect_timeout_ms)

    def get_mongodb_collection(self, db_name, collection_name, is_read_slave):
        """
        获取collection
        :param db_name:
        :param collection_name:
        :param is_read_slave: 读写分离salve
        :return:
        """
        db_obj = self.db_mapping.get(db_name, None)
        if not db_obj:
            if not self.mongodb_client:
                self.mongodb_client = self.get_mongodb_conn(
                    url=self.mongodb_url,
                    connect_timeout_ms=self.connect_timeout_ms)
            db_obj = self.mongodb_client.get_database(db_name)
            self.db_mapping[db_name] = db_obj

        if is_read_slave:
            return db_obj.get_collection(
                collection_name, read_preference=READ_SLAVE)
        else:
            return db_obj.get_collection(
                collection_name)

