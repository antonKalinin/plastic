import logging
from os import path


class Logger:

    log_dir = "/home/www/plastic/logs"

    def __init__(self, filename):
        logging.basicConfig(
            level=logging.INFO,
        )

        basename = path.basename(filename)
        log_file = path.splitext(basename)[0] + '.log'

        self.logger = logging.getLogger(basename)
        fhandler = logging.FileHandler(path.join(Logger.log_dir, log_file), "a")
        formatter = logging.Formatter("%(asctime)s %(message)s", "%Y-%m-%d %H:%M:%S")
        fhandler.setFormatter(formatter)

        self.logger.addHandler(fhandler)

    def info(self, msg):
        return self.logger.info(msg)