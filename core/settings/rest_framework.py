from datetime import timedelta
import os


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_RENDERERS_CLASSES": [
        "rest_framework_xml.renderers.XMLRenderer",
        "rest_framwork.renderers.JSONRenderer",
        "rest_framework_csv.renderers.CSVRenderer",
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'SIGNING_KEY': os.environ.get("JWT_SECRET_KEY"),
    'AUTH_HEADER_TYPES': ('Bearer',)
}