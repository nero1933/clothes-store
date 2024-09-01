from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from ecommerce.models.reviews import Review
from ecommerce.serializers.reviews import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ReviewSerializer

    def get_queryset(self):
        queryset = Review.objects \
            .select_related('order_item__order__user') \
            .filter(order_item__order__user=self.request.user)

        return queryset
