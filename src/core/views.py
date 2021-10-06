from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import Http404
from .models import Repo
from .forms import *
from .models import Repo
from sourcefa.settings import BASE_DIR,REPO_ROOT
import os

def index(request):
    repos = Repo.objects.all()
    context = {
        'repos' : repos,
    }
    return render(request, 'index.html',context)


def newrepo(request):
    form = NewRepoForm()
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NewRepoForm(request.POST)

        if form.is_valid():
            repo_name = form.cleaned_data['repo_name']
            desc = form.cleaned_data['desc']

            repo = Repo(repo_name=repo_name,user_id=request.user.username,desc=desc)
            repo.save()

            repo_path = os.path.join(BASE_DIR,REPO_ROOT,request.user.username,repo_name),
            return HttpResponseRedirect(f'/{request.user.username}/{repo_name}')

    return render(request, 'newrepo.html',{'form':form})

def viewrepo(request,user_profile,repo_name):
    if Repo.objects.filter(repo_name=repo_name,user_id=user_profile).exists():
        
        context = {
            'repo' : Repo.objects.get(repo_name=repo_name,user_id=user_profile),
        }
        return render(request,'viewrepo.html',context)
    else :
        raise Http404

def uploadrepo(request,user_profile,repo_name):
    form = FileUploadForm()
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = FileUploadForm(request.POST)

        if form.is_valid():
            commit = form.cleaned_data['commit']
            files = form.cleaned_data['files']

            repo_path = os.path.join(BASE_DIR,REPO_ROOT,request.user.username,repo_name)

            # write to repo
            #...

            return HttpResponseRedirect(f'/{request.user.username}/{repo_name}')

    return render(request, 'newrepo.html',{'form':form})