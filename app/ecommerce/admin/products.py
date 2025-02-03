from django import forms
from django.contrib import admin
from django.db.models import Prefetch, Avg

from ecommerce.models.products import *


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

    # class Media:
    #     css = {
    #         'all': ('css/admin_styles.css', )  # Load custom CSS
    #     }


class ProductItemInline(admin.StackedInline):
    model = ProductItem
    form = ProductItemForm
    formset = ChoicesFormSet
    fields = (
        'pk',
        'product',
        'color',
        'price',
        'product_code',
        'discount',
        'stripe_product_id',
        'stripe_price_id',
        'is_active',
    )
    readonly_fields = ('pk',)
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
    list_display = ('id', 'name', 'category', 'brand', 'gender', 'product_rating')
    list_display_links = ('name', )
    fieldsets = (
        ('Product Information', {
            'fields': (
                'pk',
                'name',
                'slug',
                'description',
                'gender',
                'category',
                'brand',
                'attribute_option',
                'is_active',
            )
        }),
    )
    readonly_fields = ('pk', )
    search_fields = ('name', 'category__name', 'brand__name', )
    inlines = [ProductItemInline]

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


# ----------------------------------------------------------------------------------------------------------------------


class ProductVariationChoicesFormSet(forms.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        product_pk = ProductItem.objects.get(pk=self.instance.pk).product.pk

        size_category_pk = Product.objects.select_related(
            'category__size_category'
        ).get(
            pk=product_pk
        ).category.size_category.pk

        size_choices = list(ProductSize.objects.filter(size_category=size_category_pk).values_list('pk', 'name'))
        self.form_kwargs['size_choices'] = size_choices


class ProductVariationForm(forms.ModelForm):
    """ ProductItem Model Form """

    class Meta:
        model = ProductVariation
        exclude = ()

    def __init__(self, *args, **kwargs):
        size_choices = kwargs.pop('size_choices', [((), ())])

        super().__init__(*args, **kwargs)

        self.fields['size'].choices = [('-', '---')] + size_choices
        self.fields['size'].initial = self.fields['size'].choices[0][0]
        self.fields['size'].empty_values = (self.fields['size'].choices[0][0],)


class ProductVariationInline(admin.TabularInline):
    model = ProductVariation
    form = ProductVariationForm
    formset = ProductVariationChoicesFormSet
    extra = 1

    def get_queryset(self, request):
        queryset = ProductVariation.objects.select_related(
            'product_item__product__category__size_category', # used by ProductVariationChoicesFormSet
            'product_item__color', # used by __str__ in ProductVariationModel
            'size', # used by __str__ in ProductVariationModel
        )

        return queryset


class ProductItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_item_name', 'product_code', )
    list_display_links = ('product_item_name', )
    fieldsets = (
        ('Product Information', {
            'fields': (
                'name',
                'slug',
                'description',
                'gender',
                'category',
                'brand',
                'attribute_option',
                'product_is_active',
            )
        }),
        ('Product Item Information', {
            'fields': (
                'product',
                'color',
                'price',
                'product_code',
                'discount',
                'stripe_product_id',
                'stripe_price_id',
                'is_active',
            ),
        }),
    )
    readonly_fields = (
        'name',
        'slug',
        'description',
        'gender',
        'category',
        'brand',
        'attribute_option',
        'product_is_active',
    )
    search_fields = ('product_code', 'product__name', 'color__name')
    exclude = ()
    inlines = [ProductVariationInline]

    def product_item_name(self, obj):
        return f'{obj.product.name.capitalize()} / Color: {obj.color} '

    def get_queryset(self, request):

        queryset = ProductItem.objects.select_related(
            'product__category',
            'product__brand',
            'color',
        ).prefetch_related(
            Prefetch('discount', queryset=Discount.objects.all()),
        )

        return queryset

    def name(self, obj):
        if obj.product.name:
            return obj.product.name.capitalize()

        return None

    def slug(self, obj):
        if obj.product.slug:
            return obj.product.slug

        return None

    def description(self, obj):
        if obj.product.description:
            return obj.product.description.capitalize()

        return None

    def gender(self, obj):
        if obj.product.gender:
            return obj.product.gender_display()

        return None

    def category(self, obj):
        if obj.product.category:
            return obj.product.category

        return None

    def brand(self, obj):
        if obj.product.brand:
            return obj.product.brand

        return None

    def attribute_option(self, obj):
        if obj.product.attribute_option:
            return ', '.join([option.name.capitalize() for option in obj.product.attribute_option.all()])

        return None

    def product_is_active(self, obj):
        if obj.product.is_active:
            return obj.product.is_active

        return None

admin.site.register(Product, ProductAdmin)
admin.site.register(AttributeOption)
admin.site.register(AttributeType)
admin.site.register(Brand)
admin.site.register(ProductCategory)
admin.site.register(ProductSize)
admin.site.register(SizeCategory)
admin.site.register(ProductItem, ProductItemAdmin)
admin.site.register(Color)
admin.site.register(Image)
admin.site.register(ProductVariation)
admin.site.register(Discount)