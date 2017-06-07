# DJProcess
PUT as POST for Django. 

## A self hosted batteries included "serverless" solution. 

DJProcess provides an environment for running python code _within_ your own data-center in a very configurable and secure manner. **Plus:** it comes with automatic documentation and service discovery. Furthermore you can even write code executable code and build complex business processes _from your browser_. 

You can install it as a standalone solution, or you can add it to your existing Django Projects. 

### Getting started: 

The official docker image ships with some predefined tasks

```
docker run toast38coza/djprocess
```

#### Standalone installation 

Inside the container, the following locations are relevant: 

**Tasks:**
* `/code/djprocess/tasks/core/`** # A collection of core tasks provide by default
* `/code/djprocess/tasks/custom/`** # put your custom tasks here and reference them via the path

**Validations**
* `/code/djprocess/validation/core/`** # A collection of core tasks provide by default
* `/code/djprocess/validation/custom/`** # put your custom tasks here and reference them via the path

**Configuration:**

All config variables (e.g.: Auth tokens etc) should be provided as environment variables. 

**Docs are at:**

http://localhost:4000


#### As part of an existing project

* pip install
* add to urls


### Define a process: 

**registry.py**

```

HELLO_WORLD_PROCESS = {
  id: 'hello-world',
  # meta info is used for building documentation
  meta: {
    name: 'HelloWorld',
    description: '...',    
	fields: [
		{ name: 'foo', description: '..', type: TYPES.CharField, default: None, required: True }
	]
  },
  # validation methods to verify - all must resolve true
  # a validation method will receive the request object
  validations: [ # validations are a tuple. The second item is the arguments as an array
    ('validations.required_fields', ['foo', 'bar', 'baz']), 
    ('validations.some_custom_validation',)
  ],
  # all tasks will receive the HttpRequest object as the first argument
  # synchronous tasks are run inline. If they fail, the result will be 502
  tasks_sync: [
    'tasks.say_hello'
  ]
  # async tasks are run on a queue 
  # you can optionally pass an argument which determines when the task will run. 
  tasks_async: [
    'tasks.comms.send_hello_email'
    'tasks.analytics.record_hello_hit'    
  ]
}

```

### Process API: 

**Process:**

**POST /:process_id Create a process instance (e.g.: `POST /hello-world`)

**GET /:** List processess

**Documentation**

DJProcess builds documentation for you as you go. 






