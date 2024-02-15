from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

from phonenumber_field.modelfields import PhoneNumberField


class UserProfileManager(BaseUserManager):
    """ Helps Django work with our custom user model. """

    def create_user(self, email, name, phone, password=None):
        """ Creates a new user profile object. """

        if not email:
            raise ValueError('Users must have an email address.')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, phone=phone)

        user.set_password(password)
        user.save(using=self.db)

        # Creates a shopping cart for the user
        # ShoppingCart.objects.create(user=user)

        return user

    def create_superuser(self, email, name, phone, password=None):
        """ Creates and saves a new superuser with given details. """

        user = self.create_user(email, name, phone, password)

        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.is_guest = False

        user.save(using=self.db)

        # cart_exists = len(ShoppingCart.objects.filter(user=user))
        # if not cart_exists:
        #     ShoppingCart.objects.create(user=user)

        return user

class UserProfile(AbstractBaseUser, PermissionsMixin):
    """ Represents a 'user profile' inside our system. """

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    phone = PhoneNumberField(null=True, blank=True)
    # address = models.ManyToManyField(Address, through='UserAddress', related_name='address_to_user')
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_guest = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone']

    def get_full_name(self):
        """ Used to get a users full name. """

        return self.name

    def get_short_name(self):
        """ Used to get a users short name. """

        return self.name

    def __str__(self):
        """ Convert an object to string. """

        return self.email




