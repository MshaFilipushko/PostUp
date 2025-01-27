from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, "users/main_page.html")


def about(request):
    return render(request, "users/about.html")


def contact(request):
    return render(request, "users/contact.html")