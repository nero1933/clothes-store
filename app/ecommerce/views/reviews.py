from django.db import IntegrityError

from rest_framework import mixins, serializers
from rest_framework.exceptions import PermissionDenied
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

        # try:
        #     order_item = OrderItem.objects \
        #         .only('pk', 'order_id', 'order__user__email') \
        #         .select_related('order__user') \
        #         .get(id=order_item_id, order__user=self.request.user)
        #
        #     product = Product.objects \
        #         .only('pk', 'slug') \
        #         .get(slug=product_slug)

        #     if order_item.order.user != self.request.user:
        #         raise PermissionDenied()
        # except OrderItem.DoesNotExist:
        #     raise serializers.ValidationError({"Error": "Invalid order item ID"})
        # except Product.DoesNotExist:
        #     raise serializers.ValidationError({"Error": "Invalid product slug"})

        payment = Payment.objects.only('payment_bool', 'order_id').get(order_id=order_item.order_id)
        if not payment.payment_bool:
            raise PermissionDenied()

        try:
            serializer.save(order_item=order_item, product=product)
        except IntegrityError:
            raise serializers.ValidationError({"Error": "You have already reviewed this item in this order"})



    # @action(detail=False, methods=['post'])
    # def create_review(self, request, slug=None):
    #     # Logic for creating a review
    #     return Response({"message": "Review created"})

    # @action(detail=True, methods=['patch', 'delete'])
    # def update_delete(self, request, slug=None, pk=None):
    #     if request.method == 'PATCH':
    #         # Logic to update
    #         return Response({"message": f"Review {pk} updated"})
    #     elif request.method == 'DELETE':
    #         # Logic to delete
    #         return Response({"message": f"Review {pk} deleted"})
