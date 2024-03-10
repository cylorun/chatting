import datetime

class Logging:
    @staticmethod
    def info(s):
        print(f'[INFO/{datetime.datetime.now()}] {s}')
    @staticmethod
    def warn(s):
        print(f'[WARN/{datetime.datetime.now()}] {s}')
    @staticmethod
    def error(s):
        print(f'[ERROR/{datetime.datetime.now()}] {s}')