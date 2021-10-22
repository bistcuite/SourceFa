from django.contrib import admin
from .models import *

# register Repo model
admin.site.register(Repo)
admin.site.register(Star)
