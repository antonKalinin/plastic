# import simplejson as json


class RepoCollection:
    """
        Collection of repositories
        - returns aggregated languages data
        - returns an unique list of languages
    """

    def __init__(self, data):
        self.data = data
        self.languages = {}

        for repo in self.data:
            for language in repo[u'languages']:
                if language not in self.languages:
                    self.languages[language] = 0

                self.languages[language] += repo[u'languages'][language]

    def get_languages_list(self):
        return self.languages.keys()

    def get_languages_stats(self):
        return self.languages
