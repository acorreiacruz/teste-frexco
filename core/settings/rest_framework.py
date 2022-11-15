from datetime import timedelta
import os


REST_FRAMEWORK ={
    "DEFAULT_AUTHENCIATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=120),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'SIGNING_KEY': os.environ.get("JWT_SECRET_KEY"),
    'AUTH_HEADER_TYPES': ('Bearer',),
}
