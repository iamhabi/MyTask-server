from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['pk', 'user', 'parent_uuid', 'title', 'description', 'is_done', 'due_date', 'created']