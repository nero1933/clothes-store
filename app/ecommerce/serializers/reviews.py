from rest_framework import serializers

from ecommerce.models import Review, Product, OrderItem


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    order_item = serializers.PrimaryKeyRelatedField(queryset=OrderItem.objects.all())
    comment = serializers.CharField(max_length=255)
    rating = serializers.IntegerField()
    created_at = serializers.DateTimeField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request', None)
        if request and hasattr(request, 'user'):
            self.fields['order_item'].queryset = (
                OrderItem.objects \
                    .select_related('order')
                    .filter(order__user=request.user))

    class Meta:
        model = Review
        fields = '__all__'

    def validate(self, data):
        user = data['user']
        product = data['product']

        if Review.objects.filter(user=user, product=product).exists():
            raise serializers.ValidationError('You have already reviewed this product.')

        return data
