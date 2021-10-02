from django.db import models

class User(models.Model):
    user_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField()
    created_on = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return self.user_id

class Repo(models.Model):
    repo_name = models.CharField(max_length=50)
    user_id = models.CharField(max_length=100)
    desc = models.TextField(max_length=500)
    created_on = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return self.repo_name