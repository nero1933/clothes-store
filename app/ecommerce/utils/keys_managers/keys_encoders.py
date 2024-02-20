import uuid


class KeyEncoder:
    """
    tests.
    """
    confirmation_key = None
    timeout = None

    def __init__(self, token):
        self._token = token

    @property
    def token(self):
        return self._token

    def __create_token(self):
        self._token = uuid.uuid4().hex

    def create_confirmation_key_and_token(self):
        self.__create_token()
        return self.confirmation_key.format(token=self.token), self.token
