from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Q

from rest_framework.reverse import reverse

from ecommerce.utils.products import sizes

class Product(models.Model):
    """ Model describes products. """

    class Meta:
        ordering = ('-date_created',)

    GENDER_CHOICES = [
        ('M', 'Man'),
        ('W', 'Woman'),
    ]

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.CharField(max_length=255)
    gender = models.CharField(max_length=15, choices=GENDER_CHOICES)
    category = models.ForeignKey('ProductCategory', on_delete=models.CASCADE)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
    attribute_option = models.ManyToManyField('AttributeOption')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products', kwargs={'slug': self.slug})


class AttributeOption(models.Model):
    attribute_type = models.ForeignKey('AttributeType', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class ProductCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.CharField(max_length=255)
    image = models.URLField(blank=True, null=True)
    size_category = models.ForeignKey('SizeCategory', on_delete=models.CASCADE)
    parent_category = models.ForeignKey('ProductCategory', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name


class ProductSize(models.Model):

    # Sizes are defined in utils.
    PRODUCT_SIZE_CHOICES = sizes.PRODUCT_SIZE_CHOICES

    name = models.CharField(max_length=20, choices=PRODUCT_SIZE_CHOICES, unique=True)
    size_category = models.ForeignKey('SizeCategory', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class SizeCategory(models.Model):

    # Size categories are defined in utils.
    SIZE_CATEGORY_CHOICES = sizes.SIZE_CATEGORY_CHOICES

    name = models.CharField(max_length=10, choices=SIZE_CATEGORY_CHOICES, unique=True)

    def __str__(self):
        return self.name

class ProductItem(models.Model):
    product = models.ForeignKey('Product', related_name='product_item', on_delete=models.CASCADE)
    color = models.ForeignKey('Color', on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    product_code = models.CharField(max_length=32)
    discount = models.ManyToManyField('Discount', related_name='discount', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    stripe_product_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_price_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.product.name + ' ' + self.color.name

    def get_discount_price(self):
        # !
        # Create a test for this method
        # !

        discounts = self.discount.all()
        if not discounts:
            return self.price

        # Calculate the discount price
        rate = 0
        for discount in discounts:
            rate += discount.discount_rate

        discount_price = self.price * ((100 - rate) / 100)
        return int(discount_price)


class Image(models.Model):
    product_item = models.ForeignKey('ProductItem', related_name='image', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=255)
    is_main = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['product_item'],
                condition=Q(is_main=True),
                name='unique_main_image_per_product_item'
            )
        ]

    def __str__(self):
        return f'Image for: {self.product_item}'


class ProductVariation(models.Model):
    product_item = models.ForeignKey('ProductItem', related_name='product_variation', on_delete=models.CASCADE)
    size = models.ForeignKey('ProductSize', on_delete=models.CASCADE)
    qty_in_stock = models.PositiveIntegerField()

    def __str__(self):
        return self.product_item.product.name + ' ' + self.product_item.color.name + ' ' + self.size.name


class Discount(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    discount_rate = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name


class SimpleModel(models.Model):
    """ Abstract class for all models that have only names and slugs. """

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products', kwargs={'slug': self.slug})


class Color(SimpleModel):
    """ Model contains colors. """
    pass

class AttributeType(SimpleModel):
    """ Model contains attribute types. """
    pass

class Brand(SimpleModel):
    """ Model contains brands. """
    pass