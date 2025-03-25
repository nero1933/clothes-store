import uuid

from django.core.cache import cache


class ConfirmationManager:
    """
    Manages the creation, reading, setting and deleting
    to/from cache
    of confirmation keys and flags.
    """

    def __init__(self):
        super().__init__()
        self._conf_token = None

    @property
    def conf_token(self) -> str:
        # If 'conf_token' is None, generate 'conf_token'
        if self._conf_token is None:
            self._conf_token = uuid.uuid4().hex

        return self._conf_token

    def create_confirmation_key(self, confirmation_key_template: str) -> str:
        """
        Generate a confirmation key using the provided template.

        Key contains a template with a {conf_token} parameter.
        'conf_token' can be used as a public key
        and the rest of the template should be private.
        """
        return confirmation_key_template.format(conf_token=self.conf_token)

    @staticmethod
    def create_confirmation_flag(confirmation_flag_template: str, user_id: int) -> str:
        """
        Generate a confirmation flag using the provided template.

        Flag is a pair of key (which contains 'user_id') and a bool value.
        While value is True it means that the user still has
        an active 'confirmation_key' in cache.

        'confirmation_key' doesn't contain 'user_id'
        so it is impossible to find it by 'user_id'
        """
        return confirmation_flag_template.format(user_id=user_id)


# class ConfirmationCacheManager(ConfirmationManager):
#