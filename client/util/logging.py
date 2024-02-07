import datetime, time

class Logging:
    @staticmethod
    def info(s):
        print(f'\033[92m[INFO/{datetime.datetime.now()}] {s}\033[0m')
    @staticmethod
    def warn(s):
        print(f'\033[93m[WARN/{datetime.datetime.now()}] {s}\033[0m')
    @staticmethod
    def error(s):
        print(f'\033[91m[ERROR/{datetime.datetime.now()}] {s}\033[0m')