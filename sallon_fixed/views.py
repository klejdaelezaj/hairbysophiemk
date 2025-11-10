import datetime
from django.shortcuts import render, redirect
from .forms import AppointmentForm  # ✅ moved import here
from .google_calendar import get_free_times, add_event_to_google_calendar


def home(request):
    return render(request, "sallon/home.html")

def services(request):
    return render(request, "sallon/service.html")

def gallery(request):
    return render(request, "sallon/gallery.html")

def about_us(request):
    return render(request, "sallon/about_us.html")

def contact(request):
    return render(request, "sallon/contact.html")


def book(request):
    return render(request, 'sallon/book.html')
