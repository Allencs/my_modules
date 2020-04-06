import logging


class Logger(object):
    def __init__(self, name, clevel=logging.DEBUG):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        fmt = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # log_name = "access.log"

        sh = logging.StreamHandler()
        sh.setLevel(clevel)
        sh.setFormatter(fmt)

        # fh = logging.FileHandler(log_name)
        # fh.setFormatter(fmt)
        # fh.setLevel(flevel)

        self.logger.addHandler(sh)
        # self.logger.addHandler(fh)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)





