from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Listing
from .forms import ListingModelForm



def index(request):
    active_listings = Listing.objects.filter(active=True)
    create_listings = ListingModelForm()

    if active_listings:
        return render(request, "auctions/index.html", {
            "active_listings": active_listings
        })
    else:
        return render(request, "auctions/create.html", {
            "create_listings": create_listings
        })
    
def createListing(request):
    if request.method == "POST":
        create_listings = ListingModelForm(request.POST)
        if create_listings.is_valid():
            new_listing = create_listings.save()
            return redirect('index')
    else:
        create_listings = ListingModelForm()
    
    return render(request, "auctions/create.html", {
        "create_listings": create_listings
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
