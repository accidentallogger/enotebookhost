from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, "home/index.html")

    # Follow these steps to create a PR
