from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny




@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class Permissions(APIView):
    permission_classes = [AllowAny]
    def get(self, request, format=None):
        return Response(data=request.user.get_all_permissions())
