import nested_admin

from django import forms
from django.contrib import admin
from django.db.models import Prefetch, Avg
from django.shortcuts import get_object_or_404

from ecommerce.models import Review
from ecommerce.models.products import *


class ProductVariationInline(admin.StackedInline):
    model = ProductVariation
    extra = 1


class ProductItemForm(forms.ModelForm):
    """ ProductItem Model Form """

    discounts_choices = []
    for item in Discount.objects.values('pk', 'name', 'discount_rate'):
        discounts_choices.append(
         (item['pk'], f"{item['name']} - {item['discount_rate']}%")
        )
    discount = forms.MultipleChoiceField(
        required=True,
        choices=discounts_choices
    )

    colors_choices = [('', '---------')]
    colors_choices.extend(Color.objects.values_list('pk', 'name'))
    color = forms.ChoiceField(
        required=False,
        choices=colors_choices
    )

    class Media:
        css = {
            'all': ('css/admin_styles.css',)  # Load custom CSS
        }


class ProductItemInline(admin.StackedInline):
    model = ProductItem
    form = ProductItemForm
    extra = 1

    def get_queryset(self, request):
        queryset = ProductItem.objects.select_related(
            'product',
            'color',
        ).prefetch_related(
            Prefetch('discount', queryset=Discount.objects.all()),
        )

        return queryset


class ProductAdmin(admin.ModelAdmin):
    search_fields = ('product',)
    list_select_related = True
    # list_display = ('id', 'name', 'category', 'brand', 'gender', 'total_reviews')
    # list_display_links = ('name', )
    inlines = [ProductItemInline]
    # inlines = [ReviewInline]

    # def total_reviews(self, obj):
    #     if obj.product_rating:
    #         return round(obj.product_rating, 1)
    #     else:
    #         return 0
    #
    # total_reviews.short_description = 'Reviews'

    def get_queryset(self, request):

        queryset = Product.objects.select_related(
            'category',
            'brand'
        )

        return queryset

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