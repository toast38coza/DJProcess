from django.conf.urls import url, include
from django.contrib.auth.models import User
from django.utils.module_loading import import_string
from rest_framework import routers, serializers, viewsets, mixins, response
from .models import Process, Task
from .registry import MODULE_REGISTRY
import inspect, json
import process.tasks

class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'

class ProcessSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True)
    class Meta:
        model = Process
        fields = '__all__'

# ViewSets define the view behavior.
class ProcessViewSet(viewsets.ModelViewSet):
    queryset = Process.objects.all()
    serializer_class = ProcessSerializer

class TaskRegistryViewSet(viewsets.ViewSet):

    def list(self, request):
        docs = []
        for name, mod, description in MODULE_REGISTRY:
            module_docs = {
                "name": name,
                "description": description,
            }
            tasks = []
            for name, data in inspect.getmembers(mod):

                if name.startswith('__'):
                    continue

                method = getattr(process.tasks, name)
                tasks.append({
                    'name': name,
                    'docs': inspect.getdoc(method)
                })
            module_docs['tasks'] = tasks
            docs.append(module_docs)

        return response.Response(docs)

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()

router.register(r'docs/registry/tasks', TaskRegistryViewSet, base_name='registry_tasks')
router.register(r'processes', ProcessViewSet)

