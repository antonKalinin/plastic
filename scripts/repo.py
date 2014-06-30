import sys
import json
from os import path

# Set the path
sys.path.append(path.abspath(path.join(path.dirname(__file__), '../..')))

from plastic.mappers.repo import Repo
from plastic.models.logger import Logger

# load config
config = json.load(open('../config.json'))

# init repository mapper
repo_mapper = Repo(config)

while True:
    # get last saved repo id
    last_repo_id = repo_mapper.get_last_repo_id()
    # pull repo data from GitHub via API and save to MongoDB
    results = repo_mapper.run(last_repo_id)

