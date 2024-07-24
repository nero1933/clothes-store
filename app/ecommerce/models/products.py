from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Product(models.Model):
    product_category = models.ForeignKey('ProductCategory', on_delete=models.CASCADE)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    product_description = models.CharField(max_length=255)
    product_attribute = models.ManyToManyField('AttributeOption')

    def __str__(self):
        return self.product_name


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
    brand_name = models.CharField(max_length=255)
    brand_description = models.CharField(max_length=255)

    def __str__(self):
        return self.brand_name


class ProductCategory(models.Model):
    category_name = models.CharField(max_length=255)
    category_description = models.CharField(max_length=255)
    category_image = models.URLField(blank=True, null=True)
    size_category = models.ForeignKey('SizeCategory', on_delete=models.CASCADE)
    parent_category = models.ForeignKey('ProductCategory', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.category_name


class ProductSize(models.Model):
    size_name = models.CharField(max_length=255)
    size_category = models.ForeignKey('SizeCategory', on_delete=models.CASCADE)

    def __str__(self):
        return self.size_name


class SizeCategory(models.Model):
    size_category_name = models.CharField(max_length=255)

    def __str__(self):
        return self.size_category_name

class ProductItem(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    color = models.ForeignKey('Color', on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    product_code = models.CharField(max_length=16)
    discount = models.ManyToManyField('Discount', blank=True)

    def __str__(self):
        return self.product_code


class Color(models.Model):
    color_name = models.CharField(max_length=255)

    def __str__(self):
        return self.color_name


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
    discount_name = models.CharField(max_length=255)
    discount_description = models.CharField(max_length=255)
    discount_rate = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.discount_name