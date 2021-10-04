from django.db import models

class Repo(models.Model):
    repo_name = models.CharField(max_length=50)
    user_id = models.CharField(max_length=100)
    desc = models.TextField(max_length=500)

    def __str__(self):
        return self.repo_name