from django.urls import path
from django.urls import path,include

from . import views

urlpatterns = [
   path('', views.index, name='index'),
   path('hotels/', views.HotelListView.as_view(), name='hotels'),
   path('hotel/<int:pk>', views.HotelDetailView.as_view(), name='hotel-detail'),
   path('bookings/', views.BookingListView.as_view(), name='bookings'),
   path('booking/create/room/<int:param1>/hotel/<int:param2>', views.BookingCreateView.as_view(), name='booking_create'),
   path('booking/<int:pk>/update/', views.BookingUpdateView.as_view(), name='booking_update'),
   path('booking/<int:pk>/delete/', views.BookingDeleteView.as_view(), name='booking_delete'),
]
