from django.db import IntegrityError, transaction

from rest_framework import mixins
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from ecommerce.models import OrderItem, Product, Payment
from ecommerce.models.reviews import Review
from ecommerce.serializers.reviews import ReviewSerializer


class ReviewViewSet(mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ReviewSerializer

    def get_queryset(self):
        queryset = Review.objects \
            .select_related('order_item__order__user') \
            .filter(order_item__order__user=self.request.user) \
            .only('id', 'product_id', 'order_item_id', 'comment',
                  'rating', 'created_at', 'order_item__order__user__id', )

        return queryset

    def perform_create(self, serializer):
        order_item_id = self.kwargs.get('order_item_id')
        product_slug = self.kwargs.get('product_slug')

        order_item = get_object_or_404(
            OrderItem.objects \
                .select_related('order__user') \
                .only('pk', 'order_id', 'order__user__email'),
            id=order_item_id, order__user=self.request.user
        )

        product = get_object_or_404(Product.objects.only('pk', 'slug'), slug=product_slug)

        payment = Payment.objects.only('payment_bool', 'order_id').get(order_id=order_item.order_id)
        if not payment.payment_bool:
            raise PermissionDenied()

        # Isolate the transaction for saving the serializer
        try:
            with transaction.atomic():
                serializer.save(order_item=order_item, product=product)
        except IntegrityError:
            raise ValidationError({"detail": "You have already reviewed this item in this order."})
