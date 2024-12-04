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
        try:
            user = request.headers['user']
            tasks = Task.objects.filter(user=user)

            tasks_json = []

            for task in tasks:
                tasks_json.append(task.to_json())

            return JsonResponse(
                {
                    'response': status.HTTP_200_OK,
                    'tasks': tasks_json
                },
                safe=False
            )
        except Exception as e:
            return JsonResponse(e.args, safe=False)
    
    def create(self, request, *args, **kwargs):
        try:
            user = request.headers['user']
            user = MyUser.objects.get(id=user)

            if 'parent_id' in request.data and not request.data['parent_id'] == '' and not request.data['parent_id'] == None:
                parent_id = request.data['parent_id']
            else:
                parent_id = None
            
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
                parent_id=parent_id,
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
        
    def update(self, request, *args, **kwargs):
        try:
            user = request.headers['user']
            user = MyUser.objects.get(id=user)

            task_id = kwargs['pk']

            task = Task.objects.get(id=task_id, user=user)
            updated_task = Task(**request.data)

            task.parent_id = updated_task.parent_id
            task.title = updated_task.title
            task.description = updated_task.description
            task.is_done = updated_task.is_done
            task.due_date = updated_task.due_date

            task.save()

            return JsonResponse(
                {
                    'response': status.HTTP_200_OK,
                    'task': task.to_json()
                }
            )
        except Exception as e:
            return JsonResponse(e.args, safe=False)

    def destroy(self, request, *args, **kwargs):
        try:
            user = request.headers['user']
            user = MyUser.objects.get(id=user)
           
            task_id = kwargs['pk']

            task = Task.objects.get(id=task_id, user=user)
            task.delete()

            # TODO delete sub tasks

            return JsonResponse(
                {
                    'response': status.HTTP_200_OK
                }
            )
        except Exception as e:
            return JsonResponse(e.args, safe=False)