from django.shortcuts import render
from .models import Repo

BASE_URL = "http://127.0.0.1:8000"
def index(request):
    repos = Repo.objects.all().order_by('created_on')
    context = {
        'repos' : repos,
        'BASE_URL' : BASE_URL,
    }
    return render(request, 'index.html',context)