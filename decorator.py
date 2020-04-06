import logging
import traceback


class Decorator(object):
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        print("error found")
        try:
            self.func(*args, **kwargs)
        except Exception:
            with open("error_info.log", 'a+', encoding='utf-8') as f:
                f.write("{}\n".format(self.func.__name__) + traceback.format_exc() + "\n\t")


class Logger(object):
    def __init__(self, name, clevel=logging.DEBUG, flevel=logging.DEBUG):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        # logger在类外实例化一次，避免多次实例化
        fmt = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        log_name = "{}.log".format(name)

        sh = logging.StreamHandler()
        sh.setLevel(clevel)
        sh.setFormatter(fmt)

        fh = logging.FileHandler(log_name)
        fh.setFormatter(fmt)
        fh.setLevel(flevel)

        self.logger.addHandler(sh)
        self.logger.addHandler(fh)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.error(message)

    def warning(self, message):
        self.warning(message)


def log(func):
    def inner(*args, **kwargs):
        logger = logging.getLogger("log")
        logger.setLevel(logging.DEBUG)
        fmt = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        sh = logging.StreamHandler()
        sh.setLevel(logging.DEBUG)
        sh.setFormatter(fmt)
        logger.addHandler(sh)
        logger.error("error found")
        return func(*args, **kwargs)
    return inner


class LOG(object):

    def __init__(self, args):
        self.args = args
        self.logger = logging.getLogger("log")
        self.logger.setLevel(logging.DEBUG)
        fmt = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        sh = logging.StreamHandler()
        sh.setLevel(logging.DEBUG)
        sh.setFormatter(fmt)
        self.logger.addHandler(sh)

    def __call__(self, func):
        self.func = func
        self.logger.error(self.args)

        def realfunc(*args):
            self.func(*args)
        return realfunc


def func(data_param):
    def func_outer(func_param):
        def func_inner(*args):
            if data_param == 'man':
                print("Type is man")
                func_param(*args)
            else:
                print("Type is woman")

        return func_inner

    return func_outer


@func("man")  # 等价于func_execute=func(func_execute)
def func_man():
    print("I am func_man")


@func("man")
@LOG("ERROR")
def test(*args):

    print(*args[0])


""""""""""""""
"""通用模式"""
""""""""""""""
def mydecorator(function):
    def wrapped(*args, **kwargs):
        # 在调用原始函数之前，做点什么
        result = function(*args, **kwargs)
        # 在函数调用之后，做点什么
        # 并返回结果
        return result
    # 返回wrapper作为装饰函数
    return wrapped


""""""""""""""""""""
"""类装饰器通用模式"""
""""""""""""""""""""
class DecoratorAsClass(object):
    def __init__(self, function):
        self.function = function

    def __call__(self, *args, **kwargs):
        # 在调用原始函数之前，做点什么
        result = self.function(*args, **kwargs)

        # 在调用函数之后，做点什么
        # 并返回结果
        return result


""""""""""""""""""""
"""参数化类装饰器"""
""""""""""""""""""""
def repeat(number=3):
    """
    多次重复执行装饰函数
    :param number: 重复次数，默认值为3
    :return: actual_decorator装饰函数
    """
    def actual_decorator(function):
        def wrapper(*args, **kwargs):
            result = None
            for _ in range(number):
                result = function(*args, **kwargs)
            return result  # 最后一次原始函数调用的值
        return wrapper
    return actual_decorator


@repeat(2)
def foo():
    print("foo")


from threading import RLock
lock = RLock()


def synchronized(function):
    def _synchronized(*args, **kwargs):
        lock.acquire()
        try:
            return function(*args, **kwargs)
        finally:
            lock.release()
    return _synchronized



if __name__ == '__main__':
    foo()

