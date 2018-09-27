# -*- coding: utf-8 -*-

import ConfigParser
import sys
from pymongo import MongoClient

reload(sys)
sys.setdefaultencoding('utf-8')
configParser = ConfigParser.ConfigParser()
configParser.read('../config/config.ini')


class Mongo(object):

    def __init__(self):
        self.client = MongoClient(configParser.get('mongo', 'url'),
                                  port=int(configParser.get('mongo', 'port')))
        self.db = self.client[configParser.get('mongo', 'db')]
        self.db.authenticate(configParser.get("mongo", "user"),
                             configParser.get("mongo", "password"))

    def select(self, data):
        collection = self.db.metas
        return collection.find_one(data)


Mongo = Mongo()




