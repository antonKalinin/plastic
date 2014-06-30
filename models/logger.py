import logging
from os import path


class Logger:

    log_dir = "logs"
    log_path = path.join(path.dirname(path.abspath(__file__)), '..', log_dir)
    loggers = []

    def __init__(self, filename):
        logging.basicConfig(
            level=logging.INFO,
        )

        basename = path.basename(filename)

        if basename in Logger.loggers:
            file_dir = path.split(path.dirname(filename))[1]
            basename = file_dir + '_' + basename

        Logger.loggers.append(basename)
        log_file = path.splitext(basename)[0] + '.log'

        self.logger = logging.getLogger(basename)
        fhandler = logging.FileHandler(path.join(Logger.log_path, log_file), "a")
        formatter = logging.Formatter("%(asctime)s %(message)s", "%Y-%m-%d %H:%M:%S")
        fhandler.setFormatter(formatter)

        self.logger.addHandler(fhandler)

    def info(self, msg):
        return self.logger.info(msg)