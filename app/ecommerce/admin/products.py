import nested_admin

from django import forms
from django.contrib import admin
from django.db.models import Prefetch, Avg

from ecommerce.models.products import *


class ProductVariationInline(admin.StackedInline):
    model = ProductVariation
    extra = 1


class ChoicesFormSet(forms.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        color_choices = list(Color.objects.values_list('pk', 'name'))
        discount_choices = list(Discount.objects.values_list('pk', 'name'))
        self.form_kwargs['color_choices'] = color_choices
        self.form_kwargs['discount_choices'] = discount_choices


class ProductItemForm(forms.ModelForm):
    """ ProductItem Model Form """

    class Meta:
        model = ProductItem
        exclude = ()

    def __init__(self, *args, **kwargs):
        color_choices = kwargs.pop('color_choices', [((), ())])
        discount_choices = kwargs.pop('discount_choices', [((), ())])

        super().__init__(*args, **kwargs)

        self.fields['color'].choices = [('-', '---')] + color_choices
        self.fields['color'].initial = self.fields['color'].choices[0][0]
        self.fields['color'].empty_values = (self.fields['color'].choices[0][0],)

        self.fields['discount'].choices = discount_choices

    class Media:
        css = {
            'all': ('css/admin_styles.css', )  # Load custom CSS
        }


class ProductItemInline(admin.StackedInline):
    model = ProductItem
    form = ProductItemForm
    formset = ChoicesFormSet
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
    list_display = ('id', 'name', 'category', 'brand', 'gender', 'product_rating')
    list_display_links = ('name', )
    inlines = [ProductItemInline]
    # inlines = [ReviewInline]

    def product_rating(self, obj):
        if obj.product_rating:
            return round(obj.product_rating, 1)
        else:
            return 0

    product_rating.short_description = 'Rating'

    def get_queryset(self, request):

        queryset = Product.objects.select_related(
            'category',
            'brand'
        ).prefetch_related(
            'review'
        ).annotate(
            product_rating=Avg('review__rating')
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