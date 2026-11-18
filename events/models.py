from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Organizer(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    contact_email = models.EmailField(blank=True)
    instagram_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Venue(models.Model):
    TYPE_CHOICES = [
        ("club", "Клуб"),
        ("bar", "Бар"),
        ("loft", "Лофт"),
        ("apartment", "Квартира"),
        ("outdoor", "Просто неба"),
        ("campus", "Кампус"),
        ("other", "Інше"),
    ]

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    district = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    capacity = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Event(models.Model):
    ENTRY_TYPE_CHOICES = [
        ("free", "Вхід вільний"),
        ("donation", "Вхід за донат"),
        ("ticket", "Платний квиток"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField(null=True, blank=True)
    lineup = models.TextField(blank=True)
    dress_code = models.CharField(max_length=255, blank=True)
    entry_type = models.CharField(max_length=10, choices=ENTRY_TYPE_CHOICES)
    price = models.PositiveIntegerField(default=0)
    min_donation = models.PositiveIntegerField(null=True, blank=True)
    fundraising_purpose = models.CharField(max_length=255, blank=True)
    fundraising_url = models.URLField(blank=True)
    fundraising_goal = models.PositiveIntegerField(null=True, blank=True)
    capacity = models.PositiveIntegerField()
    organizer = models.ForeignKey(
        Organizer, on_delete=models.PROTECT, related_name="events"
    )
    venue = models.ForeignKey(Venue, on_delete=models.PROTECT, related_name="events")
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="events"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["starts_at"]

    def __str__(self):
        return self.title
