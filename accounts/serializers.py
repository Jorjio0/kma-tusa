from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=254,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="Користувач з таким email вже існує.",
            )
        ],
    )
    password = serializers.CharField(write_only=True, min_length=8, max_length=128)
    password_confirm = serializers.CharField(write_only=True, max_length=128)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "password_confirm",
        ]

    def validate(self, data):
        errors = {}

        if data["password"] != data["password_confirm"]:
            errors["password_confirm"] = "Паролі не збігаються."

        user = User(username=data["username"], email=data["email"])
        try:
            validate_password(data["password"], user)
        except DjangoValidationError as error:
            errors["password"] = error.messages

        if errors:
            raise serializers.ValidationError(errors)
        return data

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        return User.objects.create_user(**validated_data)
