from rest_framework.generics import CreateAPIView

from .serializers import RegisterUserSerializer


class RegisterUserAPIView(CreateAPIView):
    """ View for registration. """

    serializer_class = RegisterUserSerializer
