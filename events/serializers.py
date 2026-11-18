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
        extra_kwargs = {"capacity": {"min_value": 1}}


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
        extra_kwargs = {"capacity": {"min_value": 1}}

    def validate(self, data):
        starts_at = data.get("starts_at")
        ends_at = data.get("ends_at")
        entry_type = data.get("entry_type")
        price = data.get("price", 0)
        min_donation = data.get("min_donation")
        fundraising_url = data.get("fundraising_url", "")
        capacity = data.get("capacity")
        venue = data.get("venue")

        errors = {}

        if ends_at and ends_at <= starts_at:
            errors["ends_at"] = "Час завершення має бути пізніше за час початку."

        if entry_type == "ticket" and price == 0:
            errors["price"] = "Для платного квитка вкажіть ціну більше 0."
        if entry_type != "ticket" and price > 0:
            errors["price"] = "Ціну вказують лише для платного квитка."

        if entry_type == "donation" and not fundraising_url:
            errors["fundraising_url"] = (
                "Для тусовки за донат вкажіть посилання на збір."
            )
        if entry_type != "donation" and min_donation:
            errors["min_donation"] = (
                "Мінімальний донат вказують лише для тусовки за донат."
            )

        if venue.capacity and capacity > venue.capacity:
            errors["capacity"] = f"Локація вміщує лише {venue.capacity} людей."

        if errors:
            raise serializers.ValidationError(errors)
        return data
