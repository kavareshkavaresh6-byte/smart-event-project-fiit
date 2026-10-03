from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .models import Event, Booking

def home(request):
    return render(request, 'myapp/home.html')


def events(request):
    events = Event.objects.all()
    return render(request, 'myapp/events.html', {'events': events})

@login_required
def booking(request, event_id):
    event = Event.objects.get(id=event_id)

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")

        booking = Booking.objects.create(
            user=request.user,
            event=event,
            name=name,
            email=email
        )

        return render(
            request,
            "myapp/confirmation.html",
            {"booking": booking}
        )

    return render(request, "myapp/booking.html", {"event": event})


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)

        return render(request, "myapp/home.html")

    return render(request, "myapp/register.html")
    


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return render(request, "myapp/home.html")

        return render(
            request,
            "myapp/login.html",
            {"error": "Invalid username or password"}
        )

    return render(request, "myapp/login.html")
def user_logout(request):
    logout(request)
    return render(request, "myapp/home.html")

def my_bookings(request):

    if not request.user.is_authenticated:
        return render(request, "myapp/login.html")

    bookings = Booking.objects.filter(user=request.user)

    return render(
        request,
        "myapp/mybookings.html",
        {"bookings": bookings}
    )