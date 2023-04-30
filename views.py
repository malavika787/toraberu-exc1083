from django.http import HttpResponse
from django.shortcuts import render
from .models import Hotel, Room, Booking
from django.views import generic
from django.urls import reverse_lazy
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
import pytz

login_url = '/quickbook/login/'

@login_required(login_url=login_url)
def index(request):
   hotels = Hotel.objects.all()
   # count_rooms = Room.objects.all().count()
   # count_bookings = Booking.objects.all().count()
   # return render(request, 'index.html', context={'count_hotels': count_hotels, 'count_rooms': count_rooms, 'count_bookings': count_bookings})
   try:
       country = request.GET.get('country')
   except:
       country = "India"
   hotels =  Hotel.objects.filter(country=country)

   return render(request, 'index.html', context={'hotels': hotels})

class HotelListView(LoginRequiredMixin, generic.ListView):
   login_url = login_url
   model = Hotel
   ordering = ['country']

class HotelDetailView(LoginRequiredMixin,generic.DetailView):
   login_url = login_url
   model = Hotel

class BookingListView(LoginRequiredMixin,generic.ListView):
   login_url = login_url
   model = Booking

class BookingCreateView(LoginRequiredMixin,generic.CreateView):
   login_url = login_url
   model = Booking
   fields = ['from_date', 'to_date', 'rooms']

   def get_form(self, form_class=None):
       form = super(BookingCreateView, self).get_form(form_class)
       form.fields['from_date'].widget = forms.widgets.SelectDateWidget()
       form.fields['to_date'].widget = forms.widgets.SelectDateWidget()
       form.fields['rooms'].choices = [(room.id, room.type) for room in Room.objects.filter(hotel=self.kwargs['param2'])]
       return form

   def form_valid(self, form):
       utc = pytz.utc
       if form.cleaned_data["to_date"] <= form.cleaned_data["from_date"]:
           form.errors['Invalid dates: '] = 'Please recheck the dates'
           return self.form_invalid(form)
       if form.cleaned_data["from_date"] <= utc.localize(datetime.datetime.today()):
           form.errors['Invalid dates: '] = 'You can\'t book on a past date'
           return self.form_invalid(form)
       return super(BookingCreateView, self).form_valid(form)

   success_url = reverse_lazy('bookings')

class BookingUpdateView(LoginRequiredMixin,generic.UpdateView):
   login_url = login_url
   model = Booking
   fields = ['from_date', 'to_date', 'rooms', 'hotel']
   success_url = reverse_lazy('bookings')

class BookingDeleteView(LoginRequiredMixin,generic.DeleteView):
   login_url = login_url
   model = Booking
   success_url = reverse_lazy('bookings')
