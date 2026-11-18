from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Category, Event, Organizer, Venue


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=50,
        validators=[
            UniqueValidator(
                queryset=Category.objects.all(),
                message="Категорія з такою назвою вже існує.",
            )
        ],
    )

    class Meta:
        model = Category
        fields = ["id", "name"]


class OrganizerSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=100,
        validators=[
            UniqueValidator(
                queryset=Organizer.objects.all(),
                message="Організатор з такою назвою вже існує.",
            )
        ],
    )

    class Meta:
        model = Organizer
        fields = [
            "id",
            "name",
            "description",
            "contact_email",
            "instagram_url",
            "created_at",
        ]


class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = [
            "id",
            "name",
            "type",
            "district",
            "address",
            "description",
            "capacity",
        ]


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "description",
            "starts_at",
            "ends_at",
            "lineup",
            "dress_code",
            "entry_type",
            "price",
            "min_donation",
            "fundraising_purpose",
            "fundraising_url",
            "fundraising_goal",
            "capacity",
            "organizer",
            "venue",
            "category",
            "created_at",
        ]
