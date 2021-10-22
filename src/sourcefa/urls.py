from django.contrib import admin
from django.urls import path, re_path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from core import views as core_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # main page url
    path('',core_views.index),

    # admin panel url
    path('admin/', admin.site.urls),
    
    # login, signup, logout pages url
    path('profile/', include('django.contrib.auth.urls')),
    path('profile/', include('user.urls')),
    
    # new repo url
    path('new/',core_views.newrepo,name='newrepo'),
    
    # view repo url
    path('<user_profile>/<repo_name>/', core_views.viewrepo,name='viewrepo'),

    # star repo url
    path('<user_profile>/<repo_name>/star', core_views.starrepo,name='starrepo'),
    path('<user_profile>/<repo_name>/unstar', core_views.unstarrepo,name='unstarrepo'),
    
    # repo files explorer url(regex based)
    re_path(r'^(?P<user_profile>[^/]+)/(?P<repo_name>[^/]+)/tree/(?P<path>.*)', core_views.treerepo,name='treerepo'),
    
    # edit repo files url(regex based)
    re_path(r'^(?P<user_profile>[^/]+)/(?P<repo_name>[^/]+)/edit/tree/(?P<path>.*)', core_views.editrepofile,name='editrepofile'),
    
    # create repo files url(regex based)
    re_path(r'^(?P<user_profile>[^/]+)/(?P<repo_name>[^/]+)/create/tree/(?P<path>.*)', core_views.createrepofile,name='createrepofile'),
    
    
    # delete repo files url(regex based)
    re_path(r'^(?P<user_profile>[^/]+)/(?P<repo_name>[^/]+)/delete/tree/(?P<path>.*)', core_views.deleterepofile,name='deleterepofile'),
    
    # upload to repo url
    path('<user_profile>/<repo_name>/upload', core_views.uploadrepo,name='uploadrepo'),
    
    # download latest source as zip file url
    path('<user_profile>/<repo_name>/download/latest', core_views.downloadlatest,name='downloadlatest'),
    
    # user profile url
    path('<user_profile>/',core_views.profile,name='profile'),
]

# include static files urls
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.REPO_URL, document_root = settings.REPO_ROOT)
urlpatterns += static(settings.ZIP_URL, document_root = settings.ZIP_ROOT)