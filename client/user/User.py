class User:
    _instance = None

    def __init__(self, data):
        self._name = data['name']
        self._date = data['date']
        self._password = data['password']
        self._email = data['email']
        self._id = data['user_id']

    @classmethod
    def get_instance(cls, data=None):
        if cls._instance is None:
            if data is not None:
                cls._instance = cls(data)
            else:
                raise ValueError("Data must be provided for the first instance.")
        return cls._instance

    def to_dict(self):
        return {
            "name":self._name,
            "date":self._date,
            "password":self._password,
            "email":self._password,
            "user_id":self._id
        }
    def get_name(self):
        return self._name

    def get_date(self):
        return self._date

    def get_password(self):
        return self._password

    def get_email(self):
        return self._email
    def get_id(self):
        return self._id
