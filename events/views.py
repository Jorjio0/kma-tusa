import logging

from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema
from rest_framework import permissions, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsAdminOrReadOnly

from .models import Category, Event, Organizer, Venue
from .serializers import (
    CategorySerializer,
    EventSerializer,
    OrganizerSerializer,
    VenueSerializer,
)

logger = logging.getLogger(__name__)

NO_TOKEN = OpenApiResponse(
    description="Немає токена або токен невалідний.",
    examples=[
        OpenApiExample(
            "Без токена",
            value={"detail": "Реквізити перевірки достовірності не надані."},
        )
    ],
)

NOT_FOUND = OpenApiResponse(
    description="Тусовки з таким id немає.",
    examples=[OpenApiExample("Не знайдено", value={"detail": "Тусовку не знайдено."})],
)

EVENT_EXAMPLE = OpenApiExample(
    "Тусовка за донат",
    request_only=True,
    value={
        "title": "Благодійна вечірка «Грудневий вайб»",
        "description": "Вечірка з діджеями, усі донати йдуть на збір.",
        "starts_at": "2026-12-12T21:00:00+02:00",
        "ends_at": "2026-12-13T03:00:00+02:00",
        "lineup": "DJ Ворон, DJ Pumpkin",
        "dress_code": "Щось блискуче",
        "entry_type": "donation",
        "price": 0,
        "min_donation": 150,
        "fundraising_purpose": "Збір на FPV-дрони",
        "fundraising_url": "https://example.com/jar/fpv-drones",
        "fundraising_goal": 50000,
        "capacity": 120,
        "organizer": 1,
        "venue": 1,
        "category": 1,
    },
)

VALIDATION_ERROR_EXAMPLE = OpenApiExample(
    "Помилки валідації",
    response_only=True,
    status_codes=["400"],
    value={
        "ends_at": ["Час завершення має бути пізніше за час початку."],
        "fundraising_url": ["Для тусовки за донат вкажіть посилання на збір."],
    },
)


class CategoryList(APIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = CategorySerializer

    @extend_schema(responses=CategorySerializer(many=True))
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            category = serializer.save()
            logger.info(
                "Категорію id=%s створено, користувач %s", category.id, request.user
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.warning(
            "Категорію не створено, помилки в полях: %s", list(serializer.errors)
        )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetail(APIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = CategorySerializer

    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            logger.warning("Категорію id=%s не знайдено", pk)
            raise NotFound("Категорію не знайдено.")

    def get(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Категорію id=%s оновлено, користувач %s", pk, request.user)
            return Response(serializer.data)
        logger.warning(
            "Категорію id=%s не оновлено, помилки в полях: %s",
            pk,
            list(serializer.errors),
        )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        category = self.get_object(pk)
        events_count = category.events.count()
        if events_count > 0:
            logger.warning(
                "Категорію id=%s не видалено: пов'язаних тусовок %s", pk, events_count
            )
            return Response(
                {
                    "detail": f"Неможливо видалити категорію {category.name}: "
                    f"у ній є тусовки ({events_count}). "
                    "Спершу перенесіть їх в іншу категорію."
                },
                status=status.HTTP_409_CONFLICT,
            )
        category.delete()
        logger.info("Категорію id=%s видалено, користувач %s", pk, request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrganizerList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = OrganizerSerializer

    @extend_schema(responses=OrganizerSerializer(many=True))
    def get(self, request):
        organizers = Organizer.objects.all()
        serializer = OrganizerSerializer(organizers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrganizerSerializer(data=request.data)
        if serializer.is_valid():
            organizer = serializer.save()
            logger.info(
                "Організатора id=%s створено, користувач %s", organizer.id, request.user
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.warning(
            "Організатора не створено, помилки в полях: %s", list(serializer.errors)
        )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrganizerDetail(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = OrganizerSerializer

    def get_object(self, pk):
        try:
            return Organizer.objects.get(pk=pk)
        except Organizer.DoesNotExist:
            logger.warning("Організатора id=%s не знайдено", pk)
            raise NotFound("Організатора не знайдено.")

    def get(self, request, pk):
        organizer = self.get_object(pk)
        serializer = OrganizerSerializer(organizer)
        return Response(serializer.data)

    def put(self, request, pk):
        organizer = self.get_object(pk)
        serializer = OrganizerSerializer(organizer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Організатора id=%s оновлено, користувач %s", pk, request.user)
            return Response(serializer.data)
        logger.warning(
            "Організатора id=%s не оновлено, помилки в полях: %s",
            pk,
            list(serializer.errors),
        )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        organizer = self.get_object(pk)
        events_count = organizer.events.count()
        if events_count > 0:
            logger.warning(
                "Організатора id=%s не видалено: пов'язаних тусовок %s",
                pk,
                events_count,
            )
            return Response(
                {
                    "detail": f"Неможливо видалити організатора {organizer.name}: "
                    f"за ним закріплені тусовки ({events_count}). "
                    "Спершу видаліть їх або передайте іншому організатору."
                },
                status=status.HTTP_409_CONFLICT,
            )
        organizer.delete()
        logger.info("Організатора id=%s видалено, користувач %s", pk, request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class VenueList(APIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = VenueSerializer

    @extend_schema(responses=VenueSerializer(many=True))
    def get(self, request):
        venues = Venue.objects.all()
        serializer = VenueSerializer(venues, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = VenueSerializer(data=request.data)
        if serializer.is_valid():
            venue = serializer.save()
            logger.info("Локацію id=%s створено, користувач %s", venue.id, request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.warning(
            "Локацію не створено, помилки в полях: %s", list(serializer.errors)
        )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VenueDetail(APIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = VenueSerializer

    def get_object(self, pk):
        try:
            return Venue.objects.get(pk=pk)
        except Venue.DoesNotExist:
            logger.warning("Локацію id=%s не знайдено", pk)
            raise NotFound("Локацію не знайдено.")

    def get(self, request, pk):
        venue = self.get_object(pk)
        serializer = VenueSerializer(venue)
        return Response(serializer.data)

    def put(self, request, pk):
        venue = self.get_object(pk)
        serializer = VenueSerializer(venue, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Локацію id=%s оновлено, користувач %s", pk, request.user)
            return Response(serializer.data)
        logger.warning(
            "Локацію id=%s не оновлено, помилки в полях: %s",
            pk,
            list(serializer.errors),
        )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        venue = self.get_object(pk)
        events_count = venue.events.count()
        if events_count > 0:
            logger.warning(
                "Локацію id=%s не видалено: пов'язаних тусовок %s", pk, events_count
            )
            return Response(
                {
                    "detail": f"Неможливо видалити локацію {venue.name}: "
                    f"у ній заплановані тусовки ({events_count}). "
                    "Спершу перенесіть їх в іншу локацію."
                },
                status=status.HTTP_409_CONFLICT,
            )
        venue.delete()
        logger.info("Локацію id=%s видалено, користувач %s", pk, request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class EventList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = EventSerializer

    @extend_schema(
        summary="Список тусовок",
        description="Доступно всім, без токена. Тусовки відсортовані за часом початку.",
        responses={200: EventSerializer(many=True)},
    )
    def get(self, request):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Створити тусовку",
        description="Лише для залогінених користувачів: заголовок Authorization: Bearer <access>.",
        request=EventSerializer,
        responses={
            201: EventSerializer,
            400: OpenApiResponse(description="Дані не пройшли перевірку."),
            401: NO_TOKEN,
        },
        examples=[EVENT_EXAMPLE, VALIDATION_ERROR_EXAMPLE],
    )
    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            event = serializer.save()
            logger.info("Тусовку id=%s створено, користувач %s", event.id, request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.warning(
            "Тусовку не створено, помилки в полях: %s", list(serializer.errors)
        )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventDetail(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = EventSerializer

    def get_object(self, pk):
        try:
            return Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            logger.warning("Тусовку id=%s не знайдено", pk)
            raise NotFound("Тусовку не знайдено.")

    @extend_schema(
        summary="Тусовка за id",
        description="Доступно всім, без токена.",
        responses={200: EventSerializer, 404: NOT_FOUND},
    )
    def get(self, request, pk):
        event = self.get_object(pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    @extend_schema(
        summary="Оновити тусовку",
        description="Лише для залогінених користувачів. Передаються всі обов'язкові поля.",
        request=EventSerializer,
        responses={
            200: EventSerializer,
            400: OpenApiResponse(description="Дані не пройшли перевірку."),
            401: NO_TOKEN,
            404: NOT_FOUND,
        },
        examples=[EVENT_EXAMPLE],
    )
    def put(self, request, pk):
        event = self.get_object(pk)
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Тусовку id=%s оновлено, користувач %s", pk, request.user)
            return Response(serializer.data)
        logger.warning(
            "Тусовку id=%s не оновлено, помилки в полях: %s",
            pk,
            list(serializer.errors),
        )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Видалити тусовку",
        description="Лише для залогінених користувачів.",
        responses={204: None, 401: NO_TOKEN, 404: NOT_FOUND},
    )
    def delete(self, request, pk):
        event = self.get_object(pk)
        event.delete()
        logger.info("Тусовку id=%s видалено, користувач %s", pk, request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)
