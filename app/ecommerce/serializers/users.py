from django.contrib.auth.hashers import check_password
from rest_framework import serializers

from ecommerce.models import UserProfile


class RegisterUserSerializer(serializers.ModelSerializer):
    """ Serializer for user registration. """

    email = serializers.EmailField()
    password_confirmation = serializers.CharField(write_only=True)

    class Meta:
        model = UserProfile
        fields = ('id', 'email', 'first_name', 'last_name', 'password', 'password_confirmation')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        """ Checks if both passwords are the same. """

        if data['password'] != data.pop('password_confirmation'):
            raise serializers.ValidationError("Passwords didn't match.")

        return data

    def create(self, validated_data):
        user = UserProfile.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        return user


class RegisterGuestSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    class Meta:
        model = UserProfile
        fields = ('email', 'access', 'refresh')


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)


class ResetPasswordSerializer(serializers.ModelSerializer):
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
        user = self.context["user"]

        if not password:
            raise serializers.ValidationError("Enter new password.")

        if len(password) < 8:
            raise serializers.ValidationError("Passwords must be at lest 8 characters.")

        if password != password_confirmation:
            raise serializers.ValidationError(f"Passwords do not match.")

        if check_password(password, user.password):
            raise serializers.ValidationError({"The new password must not match the current one."})

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
        fields = ('id', 'email', 'first_name', 'last_name')
        extra_kwargs = {'email': {'read_only': True}}