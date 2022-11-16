from . import views
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from rest_framework.permissions import AllowAny
from rest_framework.routers import SimpleRouter
from .serializers import CustomJWTSerializer
from rest_framework import schemas
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


app_name = "api"

schema_view = get_schema_view(
   openapi.Info(
      title="Frexco Test API",
      default_version='v1',
      description="API Documentation",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="antoniocorreaicruz@outlook.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[AllowAny],
)

router = SimpleRouter()
router.register(
    "users",
    views.UserModelViewSet,
    "api-user"
)

urlpatterns = [
    path("openapi/", schemas.get_schema_view(title="Frexco API Test Schema",version="1.0.0"), name="schema"),
    path('schema/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema_swagger_ui'),
    path('schema/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema_redoc'),
    path('token/', TokenObtainPairView.as_view(serializer_class=CustomJWTSerializer), name='token_obtain_pair'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += router.urls