from .processes import hello_world_process

import process.tasks

MODULE_REGISTRY = [
  ('process.tasks', process.tasks, 'General purpose tasks')
]

PROCESS_REGISTRY = {
    'hello-world': hello_world_process
}

# PROCRESS_REGISTRY.setattr(key, value)