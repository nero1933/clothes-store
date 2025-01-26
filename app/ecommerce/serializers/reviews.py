from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework import serializers

from ecommerce.models import Review, OrderItem


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    owner = serializers.SerializerMethodField()
    product = serializers.PrimaryKeyRelatedField(read_only=True)
    order_item = serializers.PrimaryKeyRelatedField(read_only=True)
    comment = serializers.CharField(max_length=255)
    rating = serializers.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = serializers.DateTimeField(read_only=True) # read_only?

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

    def get_owner(self, obj):
        return str(obj.user.first_name) + ' ' + str(obj.user.last_name)

    # def validate(self, data):
    #     user = data['user']
    #     # product = data['product']
    #     order_item = data['order_item']
    #
    #     if Review.objects.filter(user=user, order_item=order_item).exists():
    #         raise serializers.ValidationError('You have already reviewed this product in this order.')
    #
    #     return data


