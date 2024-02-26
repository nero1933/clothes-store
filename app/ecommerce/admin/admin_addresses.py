from django.contrib import admin
from ecommerce.models.models_addresses import Address, UserAddress

admin.site.register(Address)
admin.site.register(UserAddress)
