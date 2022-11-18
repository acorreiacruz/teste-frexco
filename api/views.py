from rest_framework.viewsets import ModelViewSet
from api.serializers import UserSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsOwner


User = get_user_model()

class UserModelViewSet(ModelViewSet):
    """ User ModelViewSet for make CRUD operations on API"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ["PATCH", "DELETE"]:
            return [IsOwner()]
        if self.request.method in ["POST"]:
            return [AllowAny(),]
        return super().get_permissions()