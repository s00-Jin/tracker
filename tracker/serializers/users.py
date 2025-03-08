from rest_framework import serializers


from django.contrib.auth import get_user_model
from django.conf import settings


User = get_user_model()


class RegisterCreateSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "re_password",
            "first_name",
            "last_name",
            "phone_number",
            "role",
        ]

    def validate(self, data):
        if data["password"] != data["re_password"]:
            raise serializers.ValidationError(
                {"error": "password and re_password fields didn't match"}
            )
        return data

    def create(self, validated_data):
        validated_data.pop("re_password")
        user = User.objects.create_user(**validated_data)
        return user
