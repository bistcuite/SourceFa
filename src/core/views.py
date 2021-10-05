from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Repo
from .forms import NewRepoForm
from .models import Repo

BASE_URL = "http://127.0.0.1:8000"
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
            return HttpResponseRedirect(f'/{request.user.username}/{repo_name}')

    return render(request, 'newrepo.html',{'form':form})

def viewrepo(request,user_profile,repo_name):
    if Repo.objects.filter(repo_name=repo_name,user_id=user_profile).exists():
        
        context = {
            'user_profile' : user_profile,
            'repo_name' : repo_name,
        }
        return render(request,'viewrepo.html',context)
    else :
        return HttpResponseRedirect('/404')