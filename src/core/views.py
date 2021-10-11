from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.http import Http404
from .models import Repo
from .forms import *
from .models import Repo
from os import listdir
from os.path import isfile, isdir
from sourcefa.settings import BASE_DIR,REPO_ROOT,ZIP_ROOT
import os
from django.core.files.storage import FileSystemStorage
from user.models import CustomUser
from utils.zip import *

# main page
def index(request):
    repos = Repo.objects.all()
    context = {
        'repos' : repos,
    }
    return render(request, 'index.html',context)

# new repo page
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
            
            
            repo_path = os.path.join(BASE_DIR,REPO_ROOT,request.user.username,repo_name)

            zipfile_path = os.path.join(BASE_DIR,ZIP_ROOT,request.user.username,repo_name)
            os.makedirs(zipfile_path)
            os.makedirs(repo_path)
            repo.save()
                
            return HttpResponseRedirect(f'/{request.user.username}/{repo_name}')

    return render(request, 'newrepo.html',{'form':form})

# view repo page
def viewrepo(request,user_profile,repo_name):
    if Repo.objects.filter(repo_name=repo_name,user_id=user_profile).exists():
        readme = None

        repo_path = os.path.join(BASE_DIR,REPO_ROOT,user_profile,repo_name)

        obj = os.scandir(repo_path)
        dirs = []
        files = []
        repo_is_empty = False
        for entry in obj :
            if entry.is_dir():
                dirs.append(entry.name)
            elif entry.is_file():
                files.append(entry.name)


        if "README.md" in files :
            readme = open(os.path.join(BASE_DIR,REPO_ROOT,user_profile,repo_name,"README.md"),encoding='utf-8').read()
        
        if len(dirs) == 0 and len(files) == 0:
            repo_is_empty = True
        context = {
            'repo' : Repo.objects.get(repo_name=repo_name,user_id=user_profile),
            'readme' : readme,
            'files' : files,
            'dirs' : dirs,
            'repo_is_empty' : repo_is_empty,
        }
        return render(request,'viewrepo.html',context)
    else :
        raise Http404

# commit to repo with upload page
def uploadrepo(request,user_profile,repo_name):
    form = FileUploadForm()
    if request.method == 'POST':
        form = FileUploadForm(request.POST,request.FILES)

        if form.is_valid():
            commit = form.cleaned_data['commit']
            files_names = request.FILES['files']
            files = request.FILES.getlist('files')

            repo_path = os.path.join(BASE_DIR,REPO_ROOT,request.user.username,repo_name)
            for file in files :
                with open(os.path.join(repo_path,file.name),'w') as f:
                    f.write(str(file.read()))
            zipfile_path = os.path.join(BASE_DIR,ZIP_ROOT,request.user.username,repo_name,f'{repo_name}-latest.zip')

            zipf = zipfile.ZipFile(zipfile_path, 'w', zipfile.ZIP_DEFLATED)
            zipdir(repo_path, zipf)
            zipf.close()
            return HttpResponseRedirect(f'/{request.user.username}/{repo_name}')
            
            
    context = {
        'form' : form,
        'user_id' : user_profile,
        'repo_name' : repo_name
    }
    return render(request, 'uploadrepo.html',context)

# user profile page
def profile(request,user_profile):
    if CustomUser.objects.filter(username=user_profile).exists():
        context = {
            'current_user' : CustomUser.objects.get(username=user_profile),
            'repos' : Repo.objects.filter(user_id=user_profile)
        }

        return render(request, 'profile.html',context)
    else :
        raise Http404

def treerepo(request,user_profile,repo_name,path):
    repo_path = os.path.join(BASE_DIR,REPO_ROOT,user_profile,repo_name,path)
    if isdir(repo_path):
        obj = os.scandir(repo_path)
        dirs = []
        files = []
        dir_is_empty = False
        for entry in obj :
            if entry.is_dir():
                dirs.append(entry.name)
            elif entry.is_file():
                files.append(entry.name)
        if len(dirs) == 0 and len(files) == 0:
            dir_is_empty = True
        context = {
            'repo' : Repo.objects.get(repo_name=repo_name,user_id=user_profile),
            'dir' : True,
            'dirs' : dirs,
            'files' : files,
            'dir_is_empty' : dir_is_empty,
            'path' : path,
        }
        return render(request, 'treerepo.html',context)
    elif isfile(repo_path):
        pass
    else :
        return HttpResponse(repo_path)

def downloadlatest(request,user_profile,repo_name):
    zipfile_path = os.path.join(BASE_DIR,ZIP_ROOT,user_profile,repo_name,f'{repo_name}-latest.zip')
    if isfile(zipfile_path):
        response = HttpResponse(open(zipfile_path, 'rb').read())
        response['Content-Type'] = 'application/zip'
        response['Content-Disposition'] = f'attachment; filename={repo_name}-latest.zip'
        return response
    else :
        raise Http404