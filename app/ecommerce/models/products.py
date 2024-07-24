from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework.reverse import reverse


class Product(models.Model):
    """ Model describes products. """

    class Meta:
        ordering = ('-date_created',)

    GENDER_CHOICES = [
        ('M', 'Men'),
        ('W', 'Women'),
    ]

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.CharField(max_length=255)
    gender = models.CharField(max_length=15, choices=GENDER_CHOICES)
    category = models.ForeignKey('ProductCategory', on_delete=models.CASCADE)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
    attribute = models.ManyToManyField('AttributeOption')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products', kwargs={'slug': self.slug})


class AttributeOption(models.Model):
    attribute_type = models.ForeignKey('AttributeType', on_delete=models.CASCADE)
    attribute_option_name = models.CharField(max_length=255)

    def __str__(self):
        return self.attribute_option_name


class AttributeType(models.Model):
    attribute_name = models.CharField(max_length=255)

    def __str__(self):
        return self.attribute_name


class Brand(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class ProductCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.URLField(blank=True, null=True)
    size_category = models.ForeignKey('SizeCategory', on_delete=models.CASCADE)
    parent_category = models.ForeignKey('ProductCategory', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name


class ProductSize(models.Model):

    shoes_sizes = [(str(i), str(i)) for i in range(35, 49)]
    clothes_sizes = [
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
    ]
    SIZE_CATEGORY_CHOICES = shoes_sizes + clothes_sizes

    name = models.CharField(max_length=255, choices=SIZE_CATEGORY_CHOICES)
    size_category = models.ForeignKey('SizeCategory', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class SizeCategory(models.Model):

    SIZE_CATEGORY_CHOICES = [
        ('SHOES', 'Shoes'),
        ('CLOTHES', 'Clothes'),
    ]

    name = models.CharField(max_length=8, choices=SIZE_CATEGORY_CHOICES)

    def __str__(self):
        return self.name

class ProductItem(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    color = models.ForeignKey('Color', on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    product_code = models.CharField(max_length=16)
    discount = models.ManyToManyField('Discount', blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_code


class Color(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class ProductItemImage(models.Model):
    product_item = models.ForeignKey('ProductItem', on_delete=models.CASCADE)
    product_item_image_name = models.CharField(max_length=255)
    image_filename = models.CharField(max_length=255)


class ProductVariation(models.Model):
    product_item = models.ForeignKey('ProductItem', on_delete=models.CASCADE)
    size = models.ForeignKey('ProductSize', on_delete=models.CASCADE)
    qty_in_stock = models.PositiveIntegerField()

    def __str__(self):
        return self.product_item


class Discount(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    discount_rate = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name