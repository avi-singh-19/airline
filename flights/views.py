from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from .models import *


# Create your views here.
def index(request):
    return render(request, "flights/index.html", {
        "flights": Flight.objects.all()
    })


def flight(request, flight_id):
    try:
        flight = Flight.objects.get(id=flight_id)
    except Flight.DoesNotExist:
        return render(request, "flights/error.html")

    return render(request, "flights/flight.html", {
        "flight": flight,
        "passengers": flight.passengers.all(),
        "not_passengers": Passenger.objects.exclude(flights=flight).all
    })


def book(request, flight_id):
    try:
        if request.method == "POST":
            flight = Flight.objects.get(id=flight_id)
            passenger = Passenger.objects.get(pk=int(request.POST['passenger'])) #pk = primary key
            passenger.flights.add(flight)
    except Flight.DoesNotExist or Passenger.DoesNotExit:
        return render(request, "flights/error.html")

    return HttpResponseRedirect(reverse("flight", args=(flight.id,)))
