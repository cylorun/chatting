import datetime, time

class Logging:
    def info(s):
        print(f'\033[92m[INFO/{datetime.datetime.now()}] {s}\033[0m')
        
    def warn(s):
        print(f'\033[93m[WARN/{datetime.datetime.now()}] {s}\033[0m')
        
    def error(s):
        print(f'\033[91m[ERROR/{datetime.datetime.now()}] {s}\033[0m')