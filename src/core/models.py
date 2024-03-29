from django.db import models
from user.models import CustomUser



# Repo model for repositories
class Repo(models.Model):
    repo_name = models.CharField(max_length=50) # name
    user_id = models.CharField(max_length=100) # maintainer's username of repo
    desc = models.TextField(max_length=500) # repo description
    # returns repo's name
    def __str__(self):
        return self.repo_name

class Commit(models.Model):
    repo = models.ForeignKey(Repo, on_delete=models.CASCADE)
    commit_title = models.CharField(max_length=150)

# Star model for repositories
class Star(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    repo = models.ForeignKey(Repo, on_delete=models.CASCADE)