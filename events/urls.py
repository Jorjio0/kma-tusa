from django.urls import path

from . import views

urlpatterns = [
    path("categories/", views.CategoryList.as_view()),
    path("categories/<int:pk>/", views.CategoryDetail.as_view()),
    path("organizers/", views.OrganizerList.as_view()),
    path("organizers/<int:pk>/", views.OrganizerDetail.as_view()),
    path("venues/", views.VenueList.as_view()),
    path("venues/<int:pk>/", views.VenueDetail.as_view()),
    path("events/", views.EventList.as_view()),
    path("events/<int:pk>/", views.EventDetail.as_view()),
]
