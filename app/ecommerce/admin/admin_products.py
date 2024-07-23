from django.contrib import admin
from ecommerce.models.models_products import *

admin.site.register(Product)
admin.site.register(AttributeOption)
admin.site.register(AttributeType)
admin.site.register(Brand)
admin.site.register(ProductCategory)
admin.site.register(ProductSize)
admin.site.register(SizeCategory)
admin.site.register(ProductItem)
admin.site.register(Color)
admin.site.register(ProductItemImage)