from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import string as s
from random import SystemRandom as SR


User = get_user_model()


class CustomJWTSerializer(TokenObtainPairSerializer):
    username_field = "authentication_field"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "username", "email", "birth_date","date_joined", "password"]
        read_only_fields = ["id", "date_joined"]
    
    password = serializers.CharField(write_only=True)

    def generate_password(self):
        return ''.join(SR().choices(s.ascii_letters +s.punctuation, k=12))

    def create(self, validated_data):
        password = validated_data.get("password", "")
        if not password:
            password = self.generate_password()
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user