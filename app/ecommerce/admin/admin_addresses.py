from django.contrib import admin
from ecommerce.models.addresses import Address, UserAddress

admin.site.register(Address)
admin.site.register(UserAddress)
