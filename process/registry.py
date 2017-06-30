from .processes import hello_world_process

import process.tasks.io
import process.tasks.slack
import process.tasks.foo

# this determines which modules are displayed in the registry API:
MODULE_REGISTRY = [
    process.tasks.io,
    process.tasks.slack,
    process.tasks.foo,
]

PROCESS_REGISTRY = {
    'hello-world': hello_world_process
}

# PROCRESS_REGISTRY.setattr(key, value)