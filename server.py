import sys
import flask
import simplejson as json
from os import path

# Set the path
sys.path.append(path.abspath(path.join(path.dirname(__file__), '..')))

from plastic.mappers.repo import Repo as RepoMapper
from plastic.models.repo_collection import RepoCollection

app = flask.Flask(__name__)
config = json.load(open('config.json'))
repo_mapper = RepoMapper(config)

@app.route('/')
def index():

    return flask.render_template('index/index.html', data={})

@app.route('/api/repo')
def repo_api():
    repo_data = repo_mapper.get_repos()
    repo_collection = RepoCollection(repo_data)
    data = {
        'time_limits': repo_mapper.get_time_limits(),
        'languages_list': repo_collection.get_languages_list(),
        'languages_stats': repo_collection.get_languages_stats()
    }

    return flask.Response(json.dumps(data),  mimetype='application/json')

@app.route('/api/repo/langs')
def langs_repo_api():

    repo_data = repo_mapper.get_repos()
    repo_collection = RepoCollection(repo_data)
    stats = repo_collection.get_languages_stats()

    data = [{'lang': l, 'count': c} for l, c in stats.items()]

    return flask.Response(json.dumps(data),  mimetype='application/json')

if __name__ == "__main__":
    app.run()
