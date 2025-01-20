from rest_framework import serializers

from ecommerce.models import Address, UserAddress


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = '__all__'

class UserAddressSerializer(serializers.ModelSerializer):
    # https://www.django-rest-framework.org/api-guide/validators/#currentuserdefault
    # Advanced field defaults
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    address = AddressSerializer()

    class Meta:
        model = UserAddress
        fields = ['id', 'address', 'user', 'is_default']

    def create(self, validated_data):
        # https://www.django-rest-framework.org/api-guide/serializers/#writing-create-methods-for-nested-representations
        # Writable nested representations
        address_data = validated_data.pop('address')
        address = Address.objects.create(**address_data)
        return UserAddress.objects.create(address=address, **validated_data)

    def update(self, instance, validated_data):
        # https://www.django-rest-framework.org/api-guide/serializers/#writing-create-methods-for-nested-representations
        # Writable nested representations
        address_data = validated_data.pop('address')
        address = instance.address

        instance.user = validated_data.get('user', instance.user)
        instance.is_default = validated_data.get('is_default', instance.is_default)
        instance.save()

        address.first_name = address_data.get('first_name', address.first_name)
        address.last_name = address_data.get('last_name', address.last_name)
        address.street = address_data.get('street', address.street)
        address.unit_number = address_data.get('unit_number', address.unit_number)
        address.region = address_data.get('region', address.region)
        address.city = address_data.get('city', address.city)
        address.post_code = address_data.get('post_code', address.post_code)
        address.country = address_data.get('country', address.country)
        address.phone_number = address_data.get('phone_number', address.phone_number)
        address.save()

        return instance
