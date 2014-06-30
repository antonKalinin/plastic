import abc
import pymongo
import requests
import simplejson as json


class Mapper:
    """
        Base Mapper
    """
    __metaclass__ = abc.ABCMeta

    api_url = 'https://api.github.com/'

    def __init__(self, config):
        # for pulls
        self.auth_config = config[u'auth']
        self.rate_limit = 5000  # rate limit remaining
        self.rate_reset = 0  # timestamp of rate reset
        
        # for pushes
        self.db_config = config[u'db']

        self.client = pymongo.MongoClient(
            self.db_config[u'host'], self.db_config[u'port'])
        self.db = self.client[self.db_config[u'name']]

    def get_rate_limit(self):
        return self.rate_limit

    def get_rate_reset(self):
        return int(self.rate_reset)

    def api_request(self, method, get_params={}):
        params = dict(self.auth_config.items() + get_params.items())

        response = requests.get(Mapper.api_url + method, params=params)
        if response.status_code != 200:
            pass  # TODO: Throw an exception

        self.rate_limit = int(response.headers['x-ratelimit-remaining'])
        self.rate_reset = response.headers['x-ratelimit-reset']

        # self.logger.info("Get %s; rate limit: %d" % (method, self.rate_limit))

        return json.loads(response.text)



