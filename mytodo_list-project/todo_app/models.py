from django.db import models
# import user model
from django.contrib.auth.models import User

class Todo(models.Model):
    title = models.CharField(max_length=100)
    note = models.TextField(blank=True)
    # the date of creation will be generated automatically
    createdAt = models.DateTimeField(auto_now_add=True)
    completedAt = models.DateTimeField(null=True, blank=True)
    importantCheck = models.BooleanField(default=False)
    # this todo model needs to connect with an user
    createdByUser = models.ForeignKey(User, on_delete=models.CASCADE)

    # to see the title of the Todos
    def __str__(self):
        return self.title