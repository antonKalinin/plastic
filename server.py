import json
import flask
import pymongo

app = flask.Flask(__name__)

config = json.load(open('config.json'))
client = pymongo.MongoClient(config[u'db'][u'host'], config[u'db'][u'port'])
db = client[config[u'db'][u'name']]

@app.route('/')
def index():

    return flask.render_template('index/index.html', data={})


@app.route('/api')
def api():
    data = list(db.monthly.find({'lang': {'$in': ['py', 'rb', 'php']}}, {'_id': False}))

    return flask.Response(json.dumps(data),  mimetype='application/json')

if __name__ == "__main__":
    app.run()
