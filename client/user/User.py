class User:
    _instance = None

    def __init__(self, data):
        self._name = data['name']
        self._date = data['date']
        self._password = data['password']
        self._email = data['email']

    @classmethod
    def get_instance(cls, data):
        if cls._instance is None:
            cls._instance = cls(data)
        return cls._instance

    def get_name(self):
        return self._name

    def get_date(self):
        return self._date

    def get_password(self):
        return self._password

    def get_email(self):
        return self._email