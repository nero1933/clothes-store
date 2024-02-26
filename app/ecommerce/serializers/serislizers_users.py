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


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)


class PasswordSerializer(serializers.ModelSerializer):
    """
    tests.
    """
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)
    password_confirmation = serializers.CharField(style={"input_type": "password"},write_only=True)

    class Meta:
        model = UserProfile
        fields = ('password', 'password_confirmation')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirmation = attrs.pop('password_confirmation', None)
        if len(password) < 8:
            raise serializers.ValidationError("Passwords must be at lest 8 characters.")

        if password != password_confirmation:
            raise serializers.ValidationError("Passwords do not match.")

        return attrs

    def save(self, **kwargs):
        if self.instance is None:
            raise TimeoutError('Link has been expired')

        self.instance.set_password(self.validated_data['password'])
        self.instance.save()
        return self.instance


class UserProfileSerializer(serializers.ModelSerializer):
    """
    test.
    """
    class Meta:
        model = UserProfile
        fields = ('id', 'email', 'first_name', 'last_name', 'phone')
        extra_kwargs = {'email': {'read_only': True}}