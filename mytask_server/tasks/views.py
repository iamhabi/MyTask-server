from django.http import JsonResponse

from rest_framework import status
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

        return JsonResponse(
            {
                'response': status.HTTP_200_OK,
                'tasks': list(tasks.values())
            },
            safe=False
        )
    
    def create(self, request, *args, **kwargs):
        try:
            user = request.headers['user']
            user = MyUser.objects.get(id=user)

            if 'parent_uuid' in request.data and not request.data['parent_uuid'] == '' and not request.data['parent_uuid'] == None:
                parent_uuid = request.data['parent_uuid']
                parent_uuid = Task.objects.get(uuid=parent_uuid)
            else:
                parent_uuid = None
            
            if 'title' in request.data and not request.data['title'] == None:
                title = request.data['title']
            else:
                return JsonResponse(
                    {
                        'response': status.HTTP_400_BAD_REQUEST,
                        'error': 'Title is empty'
                    },
                    safe=False
                )

            if 'description' in request.data and not request.data['description'] == None:
                description = request.data['description']
            else:
                description = None

            if 'due_date' in request.data and not request.data['due_date'] == None:
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
                    'response': status.HTTP_201_CREATED,
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
            user = MyUser.objects.get(id=user)
          
            task_id = kwargs['pk']
            
            task = Task.objects.get(uuid=task_id, user=user)
            child_tasks = Task.objects.filter(parent_uuid=task_id)

            response = JsonResponse(
                {
                    'response': status.HTTP_200_OK,
                    'task': task.to_json(),
                    'child': list(child_tasks.values())
                },
                safe=False
            )

            return response
        except Exception as e:
            return JsonResponse(e.args, safe=False)
        
    def destroy(self, request, *args, **kwargs):
        try:
            user = request.headers['user']
            user = MyUser.objects.get(id=user)
           
            task_id = kwargs['pk']

            task = Task.objects.get(uuid=task_id, user=user)
            task.delete()

            return JsonResponse(
                {
                    'response': status.HTTP_200_OK
                }
            )
        except Exception as e:
            return JsonResponse(e.args, safe=False)