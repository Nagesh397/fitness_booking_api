from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('classes', views.list_classes),
    path('book', views.book_class),
    path('bookings', views.get_bookings_by_email),
]
