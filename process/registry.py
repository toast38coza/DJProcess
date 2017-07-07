import process.tasks.io
import process.tasks.slack

# this determines which modules are displayed in the registry API:
MODULE_REGISTRY = [
    process.tasks.io,
    process.tasks.slack
]

PROCESS_REGISTRY = {
    'hello-world': 'HelloWorld',
    'hello-slack': 'HelloSlack'
}

# PROCRESS_REGISTRY.setattr(key, value)