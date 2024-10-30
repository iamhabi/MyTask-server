from django.http import JsonResponse

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated]

    def get_child(request, id):
        try:
            response = JWTAuthentication().authenticate(request)

            print(response)

            if response[1]['token_type'] == 'access':
                child = Task.objects.filter(parent=id)

                return JsonResponse(list(child.values()), safe=False)
        except Exception as exception:
            return JsonResponse(exception.args, safe=False)