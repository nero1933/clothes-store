import uuid
from datetime import datetime

from django.db import models, IntegrityError
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

from phonenumber_field.modelfields import PhoneNumberField


class UserProfileManager(BaseUserManager):
    """ Helps Django work with our custom user model. """

    def create_user(self, email, first_name, last_name, phone, password=None):
        """ Creates a new user profile object. """

        if not email:
            raise ValueError('Users must have an email address.')

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, phone=phone)

        user.set_password(password)
        user.save(using=self.db)

        # Creates a shopping cart for the user
        # ShoppingCart.objects.create(user=user)

        return user

    def create_superuser(self, email, first_name, last_name, phone=None, password=None):
        """ Creates and saves a new superuser with given details. """

        user = self.create_user(email, first_name, last_name, phone, password)

        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.is_guest = False

        user.save(using=self.db)

        # cart_exists = len(ShoppingCart.objects.filter(user=user))
        # if not cart_exists:
        #     ShoppingCart.objects.create(user=user)

        return user

    def create_guest(self):
        """ Creates and saves user as a guest. """

        def try_create_guest():
            """ Tries to create and save user as a guest. """

            email = str(uuid.uuid4()) + '@guest.user'
            password = str(uuid.uuid4())

            try:
                guest_user = UserProfile.objects.create_user(
                    email=email,
                    first_name='guest',
                    last_name='guest',
                    password=password,
                    phone=None,
                )
            except IntegrityError:
                return None

            return guest_user


        user = None

        while user is None:
            user = try_create_guest()

        user.last_login = datetime
        user.is_guest = True

        user.save(using=self.db)

        return user

class UserProfile(AbstractBaseUser, PermissionsMixin):
    """ Represents a 'user profile'. """

    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = PhoneNumberField(null=True, blank=True)
    # address = models.ManyToManyField(Address, through='UserAddress', related_name='address_to_user')
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_guest = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    def get_full_name(self):
        """ Used to get a users full name. """

        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        """ Used to get a users short name. """

        return self.first_name

    def __str__(self):
        """ Convert an object to string. """

        return self.email
