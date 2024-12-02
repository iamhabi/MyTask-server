from django.http import JsonResponse, HttpResponseBadRequest

from rest_framework.viewsets import ModelViewSet

from .models import Task, MyUser
from .serializers import TaskSerializer
from .permissions import TaskPermission


class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [TaskPermission]

    def list(self, request, *args, **kwargs):
        user = request.headers['user']
        tasks = Task.objects.filter(user=user)

        return JsonResponse(list(tasks.values()), safe=False)
    
    def create(self, request, *args, **kwargs):
        try:
            user = request.headers['user']
            user = MyUser.objects.get(id=user)

            if 'parent_uuid' in request.data and not request.data['parent_uuid'] == '':
                parent_uuid = request.data['parent_uuid']
                parent_uuid = Task.objects.get(uuid=parent_uuid)
            else:
                parent_uuid = None
            
            if 'title' in request.data:
                title = request.data['title']
            else:
                return JsonResponse(
                    {
                        'error': 'Title is empty'
                    },
                    safe=False
                )

            if 'description' in request.data:
                description = request.data['description']
            else:
                description = None

            if 'due_date' in request.data:
                due_date = request.data['due_date']
            else:
                due_date = None

            task = Task.objects.create(
                user=user,
                parent_uuid=parent_uuid,
                title=title,
                description=description,
                is_done=False,
                due_date=due_date
            )

            task.save()

            response = JsonResponse(
                {
                    'task': task.to_json()
                },
                safe=False
            )

            return response
        except Exception as e:
            return JsonResponse(e.args, safe=False)
    
    def retrieve(self, request, *args, **kwargs):
        try:
            user = request.headers['user']
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
        
    def destroy(self, request, *args, **kwargs):
        print('destroy')
        
        try:
            user = request.headers['user']
            task_id = kwargs['pk']

            task = Task.objects.get(uuid=task_id, user=user)
            result = task.delete()

            print(result)

            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            return JsonResponse(e.args, safe=False)