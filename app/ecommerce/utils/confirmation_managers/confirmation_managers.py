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


class ConfirmationCacheManager(ConfirmationManager):
    """
    Manages the caching of confirmation keys and flags.

    This class extends `ConfirmationManager` to handle the storage of
    confirmation data in Django's cache system. It provides methods to:
    - Store a confirmation key associated with a user.
    - Store a confirmation flag indicating an active confirmation key.
    - Optionally store both the key and flag together.

    The confirmation key is used for verifying user actions (e.g., email confirmation),
    while the flag helps track active confirmation states.

    Attributes:
        Inherits methods and properties from `ConfirmationManager`.
    """

    def __init__(self):
        # Initialize parent classes explicitly
        super().__init__()
        ConfirmationManager.__init__(self)

    def cache_confirmation_key(
            self,
            confirmation_key_template: str,
            user_id: int,
            timeout: int,
    ) -> None:
        """
        Set the confirmation key in the cache.

        This method takes the confirmation key template, creates a confirmation key,
        and sets it in the cache with the associated user ID.
        """

        try:
            confirmation_key = self.create_confirmation_key(confirmation_key_template)
            cache.set(confirmation_key, {'user_id': user_id}, timeout=timeout)
        except Exception as e:
            raise Exception(f"Failed to set confirmation key in cache: {e}")

    def cache_confirmation_flag(
            self,
            confirmation_flag_template: str,
            user_id: int,
            timeout: int,
    ) -> None:
        """
        Set the confirmation flag in the cache.

        This method takes the confirmation flag template, creates a confirmation flag,
        and sets it in the cache with the value True.
        """

        try:
            confirmation_flag = self.create_confirmation_flag(
                confirmation_flag_template, user_id)
            cache.set(confirmation_flag, True, timeout=timeout)
        except Exception as e:
            raise Exception(f"Failed to set confirmation key in cache: {e}")

    def cache_confirmation_data(
            self,
            confirmation_key_template: str,
            confirmation_flag_template: str,
            user_id: int,
            timeout: int,
            store_flag: bool = False,
    ) -> None:
        """
        Set both the confirmation key and the flag in the cache.

        This method calls both set_to_cache_confirmation_key and
        set_to_cache_confirmation_flag to set the confirmation key and flag in the cache.
        """

        self.cache_confirmation_key(confirmation_key_template, user_id, timeout)
        if store_flag:
            self.cache_confirmation_flag(confirmation_flag_template, user_id, timeout)
