from django.db import models

from accounts.models import MyUser

import uuid


class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='tasks', related_query_name='tasks')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, default=None)
    title = models.TextField(blank=True, null=False)
    description = models.TextField(blank=True, null=True)
    is_done = models.BooleanField(default=False, blank=True, null=False)
    due_date = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.title
    
    def to_json(self):
        return {
            'id': self.id,
            'parent': self.parent,
            'title': self.title,
            'description': self.description,
            'is_done': self.is_done,
            'due_date': self.due_date,
            'created': self.created
        }