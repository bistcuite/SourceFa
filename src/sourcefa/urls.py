from django.contrib import admin
from django.urls import path, re_path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from core import views as core_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('profile/', include('django.contrib.auth.urls')),
    path('profile/', include('user.urls')),
    
    path('',core_views.index),

    path('new/',core_views.newrepo,name='newrepo'),
    path('<user_profile>/<repo_name>/', core_views.viewrepo,name='viewrepo'),
    path('<user_profile>/<repo_name>/upload', core_views.uploadrepo,name='uploadrepo'),
    path('<user_profile>/',core_views.profile,name='profile')
    #re_path(r'^<user_profile>/<repo_name>/tree/(?P<path>[a-zA-Z0-9-\/]+)',core_views.treerepo,name='treerepo'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.REPO_URL, document_root = settings.REPO_ROOT)