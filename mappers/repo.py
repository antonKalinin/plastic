import pymongo
import simplejson as json
from base import Mapper
from plastic.models.logger import Logger


class Repo(Mapper):
    """
        - Pulling from GitHub via API
        - Pushing and fetching data from MongoDB
    """

    collection = "repositories"

    def __init__(self, config):
        self.logger = Logger(__file__)
        self.config = config
        super(Repo, self).__init__(config)

        self.collection = self.db[Repo.collection]

    def run(self, since_repo_id):
        repositories = self.api_request('repositories', {'since': since_repo_id})
        results = []

        for repo in repositories:
            repository = self.api_request('repos/' + repo['full_name'])

            doc = {
                'repo_id': repository['id'],
                'forks_count': repository['forks_count'],
                'updated_at': repository['updated_at']
            }

            repo_name = repo['full_name']

            if repository['fork']:
                repo_name = repository['parent']['full_name']

                doc['repo_id'] = repository['parent']['id']
                doc['forks_count'] = repository['parent']['forks_count']
                doc['updated_at'] = repository['parent']['updated_at']

            method = 'repos/%s/languages' % repo_name

            languages = self.api_request(method)

            if languages:
                doc['languages'] = languages
                result = self.push(doc)

                if result is not None:
                    results.append(result)

        self.logger.info("Pushed %d repositories" % len(results))
        self.logger.info("Rate limit: %d" % self.rate_limit)

        return results

    def push(self, data):
        res = self.collection.update(
            {
                'languages': data['languages'],
                'forks_count': data['forks_count'],
                'updated_at': data['updated_at']
            },
            data,
            True
        )

        return res

    def get_last_repo_id(self):
        doc = self.collection.find({}, {'repo_id': 1, '_id': 0}).sort('repo_id', pymongo.DESCENDING)[0]

        if doc is None:
            return 2150000

        self.logger.info('Started from repository ' + str(doc[u'repo_id']))

        return doc[u'repo_id']

    def get_repos(self):
        """ By default fetch repositories updated this month """

        data = list(self.collection.find({}))

        return data

    def get_time_limits(self):
        lower_limit = self.collection.find({}, {'updated_at': 1, '_id': 0}).sort('updated_at', pymongo.ASCENDING)[0]
        higher_limit = self.collection.find({}, {'updated_at': 1, '_id': 0}).sort('updated_at', pymongo.DESCENDING)[0]

        return [lower_limit, higher_limit]
