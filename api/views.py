from rest_framework.viewsets import ModelViewSet
from rest_framework_csv.renderers import CSVRenderer
from rest_framework.renderers import JSONRenderer
from drf_excel.renderers import XLSXRenderer
from api.serializers import UserSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated


User = get_user_model()

class UserModelViewSet(ModelViewSet):
    """ User ModelViewSet for make CRUD operations on API"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated,]
    renderer_classes = [JSONRenderer, CSVRenderer, XLSXRenderer]
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]
