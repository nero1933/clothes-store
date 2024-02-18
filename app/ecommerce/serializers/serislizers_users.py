from rest_framework import serializers

from ecommerce.models import UserProfile


class RegisterUserSerializer(serializers.ModelSerializer):
    """ Serializer for user registration. """

    email = serializers.EmailField()
    password_confirmation = serializers.CharField(write_only=True)

    class Meta:
        model = UserProfile
        fields = ('id', 'email', 'first_name', 'last_name', 'phone', 'password', 'password_confirmation')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        """ Checks if both passwords are the same. """

        if data['password'] != data.pop('password_confirmation'):
            raise serializers.ValidationError("Passwords didn't match.")

        return data