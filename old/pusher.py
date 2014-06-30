import pymongo
from logger import Logger


class Pusher:
    """ Class description """

    collection = "current"

    def __init__(self, config):
        self.config = config[u'db']

        self.client = pymongo.MongoClient(self.config[u'host'], self.config[u'port'])
        self.db = self.client[self.config[u'name']]

        self.logger = Logger(__file__)

    def save_commits_stat(self, commits_data):
        collection = self.db[Pusher.collection]
        ids = collection.insert(commits_data)

        self.logger.info("saved %d commits" % len(ids))

        return ids

    def push_repositories(self, repositories):
        collection_name = self.config[u'collections'][u'repositories']
        collection = self.db[collection_name]
        ids = collection.insert(repositories)

        self.logger.info("Pushed %d repositories" % len(ids))

        return ids

