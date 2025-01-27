from django.contrib import admin
from django.db.models import Prefetch, Avg

from ecommerce.models import Review
from ecommerce.models.products import *


class ProductVariationInline(admin.TabularInline):
    model = ProductVariation
    extra = 1

class ProductItemInline(admin.TabularInline):
    model = ProductItem
    extra = 1
    inlines = [ProductVariationInline]

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'brand', 'gender', 'total_reviews')
    list_display_links = ('name', )
    inlines = [ProductItemInline]
    # inlines = [ReviewInline]

    def total_reviews(self, obj):
        if obj.product_rating:
            return round(obj.product_rating, 1)
        else:
            return 0

    total_reviews.short_description = 'Reviews'

    def get_queryset(self, request):
        review_queryset = Review.objects.only('id', 'product_id', 'rating', )

        queryset = Product.objects \
            .select_related(
                'category',
                'brand'
            ) \
            .prefetch_related(
                Prefetch('review', queryset=review_queryset),
                'product_item__product_variation',
            ) \
            .annotate(product_rating=Avg('review__rating'))

        return queryset

    def get_object(self, request, object_id, from_field=None):
        queryset = Product.objects \
            .select_related(
                'category',
                'brand'
            ) \
            .prefetch_related(
                'product_item',
                'product_item__color',
                'product_item__image',
                'product_item__discount',
                'product_item__product_variation',
                'product_item__product_variation__size',
                'product_item__product_variation__order_item',
                'attribute_option',
                'attribute_option__attribute_type',
                'review',
            ) \

        try:
            return queryset.get(pk=object_id)
        except queryset.model.DoesNotExist:
            return None


# @admin.register(ProductItem)
# class ProductItemAdmin(admin.ModelAdmin):
#     search_fields = ('product_code', )


admin.site.register(Product, ProductAdmin)
admin.site.register(AttributeOption)
admin.site.register(AttributeType)
admin.site.register(Brand)
admin.site.register(ProductCategory)
admin.site.register(ProductSize)
admin.site.register(SizeCategory)
admin.site.register(ProductItem)
admin.site.register(Color)
admin.site.register(Image)
admin.site.register(ProductVariation)
admin.site.register(Discount)