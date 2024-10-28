from django.db import models

from accounts.models import MyUser

import uuid


class Task(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='tasks', related_query_name='tasks')
    title = models.CharField(max_length=255)
    created = models.DateField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.title