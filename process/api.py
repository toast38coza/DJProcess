from django.conf.urls import url, include
from django.utils.module_loading import import_string

from rest_framework import routers, serializers, viewsets, response

from .models import Process, Task
from .registry import MODULE_REGISTRY, PROCESS_REGISTRY

import inspect

class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'

class ProcessDetailSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True)
    class Meta:
        model = Process
        fields = '__all__'

class ProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Process
        fields = '__all__'


class ProcessViewSet(viewsets.ModelViewSet):

    queryset = Process.objects.all()
    serializer_class = ProcessSerializer

class ProcessRegistryViewSet(viewsets.ViewSet):

    def list(self, request):
        processess = PROCESS_REGISTRY
        return response.Response(processess)

class TaskRegistryViewSet(viewsets.ViewSet):

    def list(self, request):
        docs = []
        for mod in MODULE_REGISTRY:
            module_docs = {
                "name": mod.__name__,
                "description": inspect.getdoc(mod),
            }
            meta = getattr(mod, '__meta', None)

            if meta is not None:
                module_docs.update({"meta": meta})

            tasks = []
            for name, data in inspect.getmembers(mod):

                if name.startswith('__'):
                    continue

                behaviour = []
                try:
                    test_module = '{}.test_{}.TaskTestCase'.format(mod.__name__, name)
                    test_case = import_string(test_module)
                    tests = [method[5:].replace('_', ' ') for method in dir(test_case) if method.startswith('test_')]
                    behaviour = behaviour + tests
                except ImportError:
                    tests = None

                meta = None
                try:
                    str='{}.{}.__meta'.format(mod.__name__, name)
                    meta = import_string(str)
                except ImportError:
                    pass

                if tests is not None:
                    for testcase_name in dir(tests):
                        if testcase_name.endswith('TestCase'):
                            behaviour.append(testcase_name)

                method = getattr(mod, name)
                tasks.append({
                    'name': name,
                    'invoke_name': '{}.{}'.format(mod.__name__, name),
                    'docs': inspect.getdoc(method),
                    'meta': meta,
                    'behaviour': behaviour,
                })
            module_docs['tasks'] = tasks
            docs.append(module_docs)

        return response.Response(docs)

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()

# create processes
router.register(r'processes', ProcessViewSet, base_name='process')

router.register(r'docs/registry/processes', ProcessRegistryViewSet, base_name='registry_processes')
router.register(r'docs/registry/tasks', TaskRegistryViewSet, base_name='registry_tasks')


