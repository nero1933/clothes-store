from rest_framework import serializers
from rest_framework.fields import IntegerField

from ..models.products import ProductVariation, ProductItem
from ..models.shopping_carts import ShoppingCart, ShoppingCartItem


class ShoppingCartItemSerializer(serializers.ModelSerializer):
    product_variation = serializers.PrimaryKeyRelatedField(
        queryset=ProductVariation.objects \
            .select_related('size',
                            'product_item__product',
                            'product_item__color'
                            )
    )
    name = serializers.SerializerMethodField()
    gender = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()
    items_price = serializers.SerializerMethodField()
    items_discount_price = serializers.SerializerMethodField()

    class Meta:
        model = ShoppingCartItem
        fields = ['id', 'cart_id', 'product_variation', 'name', 'gender', 'size', 'quantity', 'items_price', 'items_discount_price']

    def get_name(self, obj):
        return obj.product_variation.product_item.product.name

    def get_gender(self, obj):
        return obj.product_variation.product_item.product.gender

    def get_size(self, obj):
        return obj.product_variation.size.name

    def get_items_price(self, obj):
        return obj.product_variation.product_item.price * obj.quantity

    def get_items_discount_price(self, obj):
        return obj.product_variation.product_item.get_discount_price() * obj.quantity

    def create(self, validated_data):
        product_variation = validated_data.pop('product_variation')
        quantity = validated_data.pop('quantity')

        cart_items = self.context['cart_items']

        existing_item = None
        # Step 1. Check If added to shopping cart item is already in cart.
        for item in cart_items:
            print(3)
            if product_variation == item.product_variation:
                # Step 1.1. Sum quantity. (If item already exists in shopping cart).
                quantity += item.quantity
                existing_item = item

        # Step 2. Check that quantity in shopping cart isn't larger than quantity in stock.
        quantity = quantity if quantity <= product_variation.qty_in_stock else product_variation.qty_in_stock

        # Step 3. If quantity is zero raise error
        if not quantity:
            raise serializers.ValidationError("Unable to add an item to shopping cart due to out of stock")

        # Step 4. If item existed in cart update quantity.
        if existing_item:
            validated_data = {'product_variation': product_variation, 'quantity': quantity}
            return self.update(existing_item, validated_data)

        # Step 5. Create cart item and return it
        return ShoppingCartItem.objects.create(
            # cart=cart,
            cart=self.context['cart'],
            product_variation=product_variation,
            quantity=quantity,
            **validated_data
        )

    def update(self, instance, validated_data):
        quantity = validated_data.pop('quantity', instance.quantity)
        product_variation = validated_data.pop('product_variation', instance.product_variation)

        instance.product_variation = product_variation
        instance.quantity = quantity if quantity <= product_variation.qty_in_stock else product_variation.qty_in_stock

        instance.save()
        return instance
