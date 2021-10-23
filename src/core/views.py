from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.http import Http404
from .models import *
from .forms import *
from .models import Repo 
from os import listdir
from os.path import isfile, isdir
from sourcefa.settings import BASE_DIR,REPO_ROOT,ZIP_ROOT
import os
from django.core.files.storage import FileSystemStorage
from user.models import CustomUser
from utils.zip import *
from utils.lang import lang

# main page
def index(request):
    # list of all repositories
    repos = Repo.objects.all()
    
    context = {
        'repos' : repos,
    }
    return render(request, 'index.html',context)

# new repo page
def newrepo(request):
    # create a 'new repo form'
    form = NewRepoForm()
    
    # if this is a POST request we need to process the form data, else return empty form for user to fill it
    if request.method == 'POST':
        # create a form instance and populate it with data from the request
        form = NewRepoForm(request.POST)

        if form.is_valid():
            # get repo name
            repo_name = form.cleaned_data['repo_name']
            # get repo desc
            desc = form.cleaned_data['desc']
            
            # create a Repo model
            repo = Repo(repo_name=repo_name,user_id=request.user.username,desc=desc)
            # repo's path on server
            repo_path = os.path.join(BASE_DIR,REPO_ROOT,request.user.username,repo_name)
            # zip file path
            zipfile_path = os.path.join(BASE_DIR,ZIP_ROOT,request.user.username,repo_name)
            
            # make repo directories
            os.makedirs(zipfile_path)
            os.makedirs(repo_path)
            # save repo information to database
            repo.save()
                
            return HttpResponseRedirect(f'/{request.user.username}/{repo_name}')
    # if this is not a POST request we handle empty new repo form
    return render(request, 'newrepo.html',{'form':form})

# view repo page
def viewrepo(request,user_profile,repo_name):
    # if requested repo is exists, handles repo page, else return 404 error
    if Repo.objects.filter(repo_name=repo_name,user_id=user_profile).exists():
        repo = Repo.objects.get(repo_name=repo_name,user_id=user_profile)
        # is repo has readme file on root folder
        readme = None
        # stars count
        stars = 0
        # is user starred repo ?
        starred = False
        # repo's path on server
        repo_path = os.path.join(BASE_DIR,REPO_ROOT,user_profile,repo_name)
        
        # get list of dirs and files name
        obj = os.scandir(repo_path)
        dirs = []
        files = []
        repo_is_empty = False
        for entry in obj :
            if entry.is_dir():
                dirs.append(entry.name)
            elif entry.is_file():
                files.append(entry.name)

        # is readme exists ?
        if "README.md" in files :
            readme = open(os.path.join(BASE_DIR,REPO_ROOT,user_profile,repo_name,"README.md"),encoding='utf-8').read()
        
        # is repo empty ?
        if len(dirs) == 0 and len(files) == 0:
            repo_is_empty = True
        
        # get stars count
        if Star.objects.filter(repo=repo).exists() :
            stars = len(Star.objects.filter(repo=repo))
        
        # is user starred the repo ?
        if request.user.is_authenticated and Star.objects.filter(repo=repo,user=request.user).exists():
            starred = True
        context = {
            'repo' : repo,
            'readme' : readme,
            'files' : files,
            'dirs' : dirs,
            'repo_is_empty' : repo_is_empty,
            'stars' : stars,
            'starred' : starred,
        }
        return render(request,'viewrepo.html',context)
    else :
        raise Http404

# commit to repo with upload page
def uploadrepo(request,user_profile,repo_name):
    # create a upload file form
    form = FileUploadForm()
    # if this is a POST request we need to process the form data, else return empty form for user to fill it
    if request.method == 'POST':
        # create a form instance and populate it with data from the request
        form = FileUploadForm(request.POST,request.FILES)
        
        if form.is_valid():
            commit = form.cleaned_data['commit'] # get commit title
            files_names = request.FILES['files'] # get uploaded files name
            files = request.FILES.getlist('files') # get files content
            # repo path on server
            repo_path = os.path.join(BASE_DIR,REPO_ROOT,request.user.username,repo_name)
            
            # write files to repo folder on server
            for file in files :
                with open(os.path.join(repo_path,file.name),'w',encoding="utf-8") as f:
                    f.write(file.read().decode("utf-8") )
            # create zip file from latest repo's source
            zipfile_path = os.path.join(BASE_DIR,ZIP_ROOT,request.user.username,repo_name,f'{repo_name}-latest.zip')
            with zipfile.ZipFile(zipfile_path, 'w', zipfile.ZIP_DEFLATED) as zipf :
                zipdir(repo_path, zipf)
            return HttpResponseRedirect(f'/{request.user.username}/{repo_name}')

    context = {
        'form' : form,
        'user_id' : user_profile,
        'repo_name' : repo_name
    }
    return render(request, 'uploadrepo.html',context)

# user profile page
def profile(request,user_profile):
    # if user is exists show user's information, else return 404 error
    if CustomUser.objects.filter(username=user_profile).exists():
        context = {
            # get user's information
            'current_user' : CustomUser.objects.get(username=user_profile),
            # get user's repos
            'repos' : Repo.objects.filter(user_id=user_profile)
        }
        return render(request, 'profile.html',context)
    else :
        raise Http404

# explore repo files
def treerepo(request,user_profile,repo_name,path):
    # repo path on server
    repo_path = os.path.join(BASE_DIR,REPO_ROOT,user_profile,repo_name,path)
    
    # check if requested path is directory, show directory tree
    if isdir(repo_path):
        # get list of dirs and files on path
        obj = os.scandir(repo_path)
        dirs = []
        files = []
        dir_is_empty = False
        for entry in obj :
            if entry.is_dir():
                dirs.append(entry.name)
            elif entry.is_file():
                files.append(entry.name)
        # is dir is empty ?
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
    # check if requested path is a file, show file content
    elif isfile(repo_path):
        is_picture = False
        file = None
        content = None
        filename = None
        language = None
        readme = False
        if path.endswith(".png") or path.endswith(".jpg") :
            is_picture = True
            filename = os.path.basename(os.path.join(user_profile,repo_name,path)) 
        if is_picture != True :
            # read the file
            file = open(repo_path,encoding="utf-8")
            content = str(file.read())
            # get file name
            filename = os.path.basename(file.name) 
            file.close()
            # get type of file for highlight it with prism.js
            language = lang(filename)
        
        # check if requested file is a markdown file
        if language == "md" : 
            readme = True
        context = {
            'repo' : Repo.objects.get(repo_name=repo_name,user_id=user_profile),
            'file' : True,
            'content' : content,
            'filename' : filename,
            'path' : path,
            'language' : language,
            'readme' : readme,
            'is_picture' : is_picture,
        }
        return render(request, 'treerepo.html',context)
    else :
        return HttpResponse(repo_path)

# download latest source of repo
def downloadlatest(request,user_profile,repo_name):
    # zip path on server
    zipfile_path = os.path.join(BASE_DIR,ZIP_ROOT,user_profile,repo_name,f'{repo_name}-latest.zip')
    # check if it's exists, else return 404 error
    if isfile(zipfile_path):
        # download the zip file
        response = HttpResponse(open(zipfile_path, 'rb').read())
        response['Content-Type'] = 'application/zip'
        response['Content-Disposition'] = f'attachment; filename={repo_name}-latest.zip'
        return response
    else :
        raise Http404

# create file in repo page
def createrepofile(request,user_profile,repo_name,path):
    # repo path on server
    repo_path = os.path.join(BASE_DIR,REPO_ROOT,user_profile,repo_name,path)

# edit file in repo page
def editrepofile(request,user_profile,repo_name,path):
    # repo path on server
    repo_path = os.path.join(BASE_DIR,REPO_ROOT,user_profile,repo_name,path)
    if isfile(repo_path) and request.method !='POST':
        # read the file
        file = open(repo_path,encoding="utf-8")
        content = str(file.read())
        rows = len(file.readlines())
        # get file name
        filename = os.path.basename(file.name) 
        file.close()
        # get type of file for highlight it with prism.js
        language = lang(filename)

        context = {
            'repo' : Repo.objects.get(repo_name=repo_name,user_id=user_profile),
            'file' : True,
            'content' : content,
            'filename' : filename,
            'path' : path,
            'language' : language,
            'rows' : rows,
        }
        return render(request, 'editrepofile.html',context)
    elif isfile(repo_path) and request.method == 'POST' and request.user.username == user_profile :
        filename = request.POST.get('filename','')
        content = request.POST.get('content','')
        commit = request.POST.get('commit','')
        with open(repo_path,"w",encoding="utf-8") as f :
            f.write(content)
        zipfile_path = os.path.join(BASE_DIR,ZIP_ROOT,request.user.username,repo_name,f'{repo_name}-latest.zip')
        with zipfile.ZipFile(zipfile_path, 'w', zipfile.ZIP_DEFLATED) as zipf :
            zipdir(repo_path, zipf)
        return HttpResponseRedirect(f'/{user_profile}/{repo_name}/tree/{path}')
    else :
        raise Http404

# delete file in repo page
def deleterepofile(request,user_profile,repo_name,path):
    # repo path on server
    repo_path = os.path.join(BASE_DIR,REPO_ROOT,user_profile,repo_name,path)

# star repo api
def starrepo(request,user_profile,repo_name):
    if request.method == "POST" :
        repo = Repo.objects.get(repo_name=repo_name,user_id=user_profile)
        star = Star(repo=repo,user=request.user)
        star.save()
    return HttpResponseRedirect(f'/{user_profile}/{repo_name}')
    
# unstar repo api
def unstarrepo(request,user_profile,repo_name):
    if request.method == "POST" :
        repo = Repo.objects.get(repo_name=repo_name,user_id=user_profile)
        star = Star.objects.get(repo=repo,user=request.user)
        star.delete()
      
    return HttpResponseRedirect(f'/{user_profile}/{repo_name}')