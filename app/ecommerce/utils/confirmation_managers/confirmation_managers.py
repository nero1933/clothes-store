import uuid

from typing import Any

from django.core.cache import cache

from rest_framework.exceptions import ValidationError


class ConfirmationToken:
    """
    Manages handling of conf_token.
    """

    def __init__(self):
        self._conf_token = None

    @property
    def conf_token(self) -> str:
        """
        Returns a new confirmation token if one doesn't exist.
        """
        if self._conf_token is None:
            self._conf_token = uuid.uuid4().hex

        return self._conf_token


class ConfirmationManager(ConfirmationToken):
    """
    Manages handling of confirmation keys.
    """

    @staticmethod
    def create_confirmation_key(template: str, key_template: str) -> str:
        """
        Creates a confirmation key from a template and key template.
        """
        try:
            return template.format(key_template=key_template)
        except Exception as e:
            raise Exception(f"Failed create confirmation key: {e}")


class ConfirmationCacheManager(ConfirmationManager):
    """
    Manages confirmation keys and counter values in the cache.
    """

    confirmation_key_template: str
    timeout_key: int

    confirmation_counter_template: str
    timeout_counter: int

    max_attempts: int

    def cache_confirmation_data(
            self,
            template: str,
            key_template: str,
            data: Any,
            timeout: int,
    ) -> str:
        """
        Set the confirmation data in the cache.

        This method creates a confirmation key from the template,
        sets it in the cache with the provided data,
        and applies a timeout for expiry.
        """
        try:
            confirmation_key = self.create_confirmation_key(template, key_template)
            cache.set(confirmation_key, data, timeout=int(timeout))
            return confirmation_key
        except Exception as e:
            raise Exception(f"Failed to set confirmation data ({data}) in cache: {e}")

    def cache_renewed_confirmation_key(self, counter_key: str, counter_value: dict) -> None:
        """
        Renew the confirmation key in the cache by incrementing the counter value.
        This method clears the previous counter data and updates the cache with a new key and counter value.
        """
        try:
            confirmation_key = list(counter_value.keys())[0] # Get the old confirmation key
            counter = counter_value[confirmation_key]
            counter += 1 # Increment the counter

            # Delete the old confirmation key from cache
            cache.delete(confirmation_key)

            # Create a new confirmation key
            new_confirmation_key = self.create_confirmation_key(
                self.confirmation_key_template, self.conf_token
            )
            # Clear the old counter value
            counter_value.clear()
            # Set the new confirmation key with incremented counter
            counter_value.update({new_confirmation_key: counter})

            # Save the renewed counter data in the cache
            cache.set(counter_key, counter_value)

        except Exception as e:
            raise Exception(f"Failed to cache renewed confirmation key: {e}")

    def cache_confirmation_key_with_counter(
            self,
            user_id: int
    ) -> None:
        """
        Cache the confirmation_key and the counter_key for a user.

        Value of confirmation_key is {'user_id': user_id}
        Value of counter_key is {confirmation_key: 1}
        """
        try:
            confirmation_key = self.cache_confirmation_data(
                self.confirmation_key_template,
                self.conf_token,
                {'user_id': user_id},
                self.timeout_key,
            )
            # Store the confirmation counter with an initial value of 1
            self.cache_confirmation_data(
                self.confirmation_counter_template,
                str(user_id),
                {confirmation_key: 1},
                self.timeout_counter,
            )
        except Exception as e:
            raise Exception(f"Failed to cache new confirmation key: {e}")

    def handle_cache_confirmation(self, user_id: int) -> None:
        """
        Handle the caching of the confirmation key and counter for a user.
        If the counter exceeds the max attempts, raise an exception.
        If the counter does not exist, cache a new confirmation key with counter 1.
        """
        counter_key = self.create_confirmation_key(
            self.confirmation_counter_template, str(user_id)
        )

        counter_value = cache.get(counter_key, None)
        if counter_value is None:
            # If no counter exists, create a new confirmation key and counter 1
            self.cache_confirmation_key_with_counter(user_id)
            return None

        counter = list(counter_value.values())[0]
        if counter >= self.max_attempts:
            # If the max attempts are reached, raise an error
            raise ValidationError(
                "Max attempts was reached, please wait 24 hours!",
            )

        # If counter is not exceeded, renew the confirmation key and increment the counter
        self.cache_renewed_confirmation_key(counter_key, counter_value)
        return None
