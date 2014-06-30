import json
import datetime
import pymongo
from os import path
from logger import Logger


class Aggregator:
    """
        Aggregates commits stats into 3 collections:
        by month, by day and by hour.
        Clear current collection after work.
        By default should be called by cron every hour.
    """

    commits_collection = "current"
    monthly_collection = "monthly"
    daily_collection = "daily"
    hourly_collection = "hourly"

    def __init__(self, config):
        self.config = config[u'db']

        self.client = pymongo.MongoClient(self.config[u'host'], self.config[u'port'])
        self.db = self.client[self.config[u'name']]

        self.logger = Logger(__file__)

    def clear(self):
        self.db.current.remove({})
        self.logger.info('Current collection cleared up.')
        # if it's a new day, clear all last day hourly static
        if datetime.datetime.hour == 1:
            self.db[Aggregator.hourly_collection].remove({})
            self.logger.info('Hourly collection cleared up.')
            # if it's a new month, clear all last month daily static
            if datetime.datetime.day == 1:
                self.db[Aggregator.daily_collection].remove({})
                self.logger.info('Daily collection cleared up.')

    def run(self):
        commits = self.db[Aggregator.commits_collection]
        commits_data = commits.find()

        commit_date = commits_data[0][u'_id'].generation_time.timetuple()
        dates = list(commit_date[1:3])  # month and day
        # add previous hour
        hour = datetime.datetime.now().timetuple()[3] - 1
        hour = [hour, 23][hour == -1]
        dates.append(hour)
        collections = [
            self.db[Aggregator.monthly_collection],
            self.db[Aggregator.daily_collection],
            self.db[Aggregator.hourly_collection],
        ]
        lang_data = {}

        for commit in commits_data:
            for lang in commit[u'data']:
                if lang not in lang_data:
                    lang_data[lang] = 0
                lang_data[lang] += commit[u'data'][lang]

        for i in range(3):
            collection = collections[i]
            for lang in lang_data:
                collection.update(
                    {"lang": lang, "date": dates[i]},
                    {"$inc": {"count": lang_data[lang]}},
                    True
                )

        # clear current collection after all
        self.clear()

        
if __name__ == "__main__":
    # load config
    configPath = path.join(path.dirname(path.realpath(__file__)), '..', 'config.json')
    config = json.load(open(configPath))

    aggregator = Aggregator(config)
    aggregator.run()