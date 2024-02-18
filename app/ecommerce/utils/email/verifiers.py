# from django.core.cache import cache
#
# from rest_framework import status
# from rest_framework.generics import get_object_or_404
# from rest_framework.response import Response
#
# from app import settings
# from ecommerce.models import UserProfile
#
#
# class VerifyRegistrationEmail:
#     """
#     test.
#     """
#     def send_registration_link(self, token: str):
#         """
#         test.
#         """
#         registration_key = settings.USER_CONFIRMATION_KEY.format(token=token)
#         user_info = cache.get(registration_key) or {}
#
#         if user_id := user_info.get('user_id'):
#             user = get_object_or_404(UserProfile, pk=user_id)
#             user.is_active = True
#             user.save(update_fields=['is_active'])
#             cache.delete(registration_key)
#             return Response({'message': 'Successfully registered'}, status=status.HTTP_204_NO_CONTENT)
#         else:
#             return Response(status=status.HTTP_400_BAD_REQUEST)