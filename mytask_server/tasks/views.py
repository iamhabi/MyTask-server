from django.http import JsonResponse

from rest_framework.viewsets import ModelViewSet

from .models import Task
from .serializers import TaskSerializer
from .permissions import TaskPermission


class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [TaskPermission]

    def list(self, request, *args, **kwargs):
        user = request.data['user']
        tasks = Task.objects.filter(user=user)

        return JsonResponse(list(tasks.values()), safe=False)
    
    def retrieve(self, request, *args, **kwargs):
        try:
            user = request.data['user']
            task_id = kwargs['pk']
            
            task = Task.objects.get(uuid=task_id, user=user)
            child_tasks = Task.objects.filter(parent_uuid=task_id)

            response = JsonResponse(
                {
                    'task': task.to_json(),
                    'child': list(child_tasks.values())
                },
                safe=False
            )

            return response
        except Exception as e:
            return JsonResponse(e.args, safe=False)