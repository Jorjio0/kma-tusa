from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, Event, Organizer, Venue
from .serializers import (
    CategorySerializer,
    EventSerializer,
    OrganizerSerializer,
    VenueSerializer,
)


class CategoryList(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetail(APIView):
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
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
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        category = self.get_object(pk)
        events_count = category.events.count()
        if events_count > 0:
            return Response(
                {
                    "detail": f"Неможливо видалити категорію {category.name}: "
                    f"у ній є тусовки ({events_count}). "
                    "Спершу перенесіть їх в іншу категорію."
                },
                status=status.HTTP_409_CONFLICT,
            )
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrganizerList(APIView):
    def get(self, request):
        organizers = Organizer.objects.all()
        serializer = OrganizerSerializer(organizers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrganizerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrganizerDetail(APIView):
    def get_object(self, pk):
        try:
            return Organizer.objects.get(pk=pk)
        except Organizer.DoesNotExist:
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
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        organizer = self.get_object(pk)
        events_count = organizer.events.count()
        if events_count > 0:
            return Response(
                {
                    "detail": f"Неможливо видалити організатора {organizer.name}: "
                    f"за ним закріплені тусовки ({events_count}). "
                    "Спершу видаліть їх або передайте іншому організатору."
                },
                status=status.HTTP_409_CONFLICT,
            )
        organizer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class VenueList(APIView):
    def get(self, request):
        venues = Venue.objects.all()
        serializer = VenueSerializer(venues, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = VenueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VenueDetail(APIView):
    def get_object(self, pk):
        try:
            return Venue.objects.get(pk=pk)
        except Venue.DoesNotExist:
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
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        venue = self.get_object(pk)
        events_count = venue.events.count()
        if events_count > 0:
            return Response(
                {
                    "detail": f"Неможливо видалити локацію {venue.name}: "
                    f"у ній заплановані тусовки ({events_count}). "
                    "Спершу перенесіть їх в іншу локацію."
                },
                status=status.HTTP_409_CONFLICT,
            )
        venue.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EventList(APIView):
    def get(self, request):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventDetail(APIView):
    def get_object(self, pk):
        try:
            return Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            raise NotFound("Тусовку не знайдено.")

    def get(self, request, pk):
        event = self.get_object(pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def put(self, request, pk):
        event = self.get_object(pk)
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        event = self.get_object(pk)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
