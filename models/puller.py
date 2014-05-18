import json
from os import path

import requests

from logger import Logger


class Puller:
    """ Class for pulling data from GitHub via API """

    def __init__(self, config):
        self.auth_params = config[u'auth']
        self.rate_limit = 5000  # rate limit remaining
        self.rate_reset = 0  # timestamp of rate reset

        self.logger = Logger(__file__)

    def get_rate_limit(self):
        return self.rate_limit

    def get_rate_reset(self):
        return int(self.rate_reset)

    def get_commits_stat(self):
        """
        returned data looks like:
        [
            {
                "cid": commit_id,
                "data" {
                    "js": 12,
                    "php": 23,
                    "html": 33
                }
            }
        ]
        """
        # get events
        response = requests.get('https://api.github.com/events', params=self.auth_params)
        if response.status_code != 200:
            pass  # TODO: Throw an exception

        self.rate_limit = int(response.headers['x-ratelimit-remaining'])
        self.rate_reset = response.headers['x-ratelimit-reset']

        self.logger.info("get events; rate limit: %d" % self.rate_limit)

        # filter push events
        events = json.loads(response.text)
        push_events = [event for event in events if event[u'type'] == 'PushEvent']

        if len(push_events) == 0:
            return False

        # fetch commits
        commits = []
        commits_stat = []

        for event in push_events:
            commits += event[u'payload'][u'commits']

        commits_urls = [commit[u'url'] for commit in commits]

        for commit_url in commits_urls:
            files_stat = {}
            commit_id = commit_url.split('/')[-1]
            commit = requests.get(commit_url, params=self.auth_params)
            commit_data = json.loads(commit.text)

            # update rate limit and reset time
            self.rate_limit -= 1
            self.rate_reset = commit.headers['x-ratelimit-reset']

            if u'files' in commit_data:
                file_names = [file_obj[u'filename'] for file_obj in commit_data[u'files']]
                file_types = [path.splitext(filename)[1] for filename in file_names]
                if len(file_types) > 0:
                    for file_type in file_types:
                        if file_type not in files_stat:
                            files_stat[file_type[1:]] = file_types.count(file_type)

            commits_stat.append({"cid": commit_id, "data": files_stat})

        self.logger.info("returning %d commits; rate limit: %d" % (len(commits_stat), self.rate_limit))

        return commits_stat