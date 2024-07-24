from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from ecommerce.models.addresses import UserAddress
from ecommerce.serializers.addresses import UserAddressSerializer


class UserAddressViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserAddressSerializer
    lookup_field = 'pk'
    http_method_names = ['get', 'post', 'patch', 'delete', 'options']

    def get_queryset(self):
        queryset = UserAddress.objects.filter(user=self.request.user) \
            .select_related('address')

        return queryset
