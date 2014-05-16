import time
import json
from models.puller import Puller
from models.pusher import Pusher
from models.logger import Logger

# load config
config = json.load(open('config.json'))

# init puller and pusher
puller = Puller(config)
pusher = Pusher(config)

logger = Logger(__file__)

rate_limit = puller.get_rate_limit()
pull_speed = 1.4

while rate_limit > 0:
    logger.info('*' * 20 + ' new loop ' + '*' * 20)
    rate_limit = puller.get_rate_limit()
    rate_reset = puller.get_rate_reset()
    current_ts = int(time.time())

    if rate_reset:
        remaining_time = rate_reset - current_ts
        current_pull_speed = rate_limit / float(remaining_time)

        logger.info('rate limit %d' % rate_limit)
        logger.info('remaining time %d' % remaining_time)
        logger.info('current pull speed %f req/sec' % current_pull_speed)

        speed_delta = current_pull_speed - pull_speed

        if speed_delta > 0:
            sleep_time = int(len(commits_stats) * speed_delta)
            if sleep_time > 1:
                logger.info('sleep for %d secs' % sleep_time)
                time.sleep(sleep_time)



    commits_stats = puller.get_commits_stat()
    pusher.save_commits_stat(commits_stats)


