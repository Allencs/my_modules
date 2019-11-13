import logging
import traceback


class Logger(object):

    def __init__(self, *args, **kwargs):
        log_level = None
        self.level = args[0]
        self.logger = logging.getLogger(kwargs['name'])
        if self.level == "DEBUG":
            log_level = logging.DEBUG
        elif self.level == "INFO":
            log_level = logging.INFO
        elif self.level == "WARNING":
            log_level = logging.WARNING
        elif self.level == "ERROR":
            log_level = logging.ERROR

        self.logger.setLevel(log_level)
        fmt = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        sh = logging.StreamHandler()
        sh.setLevel(log_level)
        sh.setFormatter(fmt)
        self.logger.addHandler(sh)

    def __call__(self, function):
        def wrapper(*args, **kwargs):
            try:
                function(*args, **kwargs)
            except Exception as e:
                self.logger.error("<FunctionName: {}> {}".format(function.__name__, e))
        return wrapper


def ErrorInfo(func):
    def inner_func(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception:
            print("******ERROR FOUND******")
            with open("error_info.log", 'a+', encoding='utf-8') as f:
                f.write("{}\n".format(func.__name__) + traceback.format_exc() + "\n\t")
    return inner_func


if __name__ == '__main__':
    # Test().foo()
    pass
