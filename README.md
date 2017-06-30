# DJProcess
PUT as POST for Django.

## A self hosted batteries included "serverless" solution.

DJProcess provides an environment for running python code _within_ your own data-center in a very configurable and secure manner. **Plus:** it comes with automatic documentation and service discovery. Furthermore you can even write code executable code and build complex business processes _from your browser_.

## Objectives:

* A pattern for exposing application functionality in a scaleable manner (scaleable in terms of: it works on big projects).
* Easy to get started
* Easy to deploy
* East to test
* Decoupled
* Auto-documenting


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

## Tasks

Tasks are atomic pieces of code (functions really).
Tasks should do only one thing.

**Add a task:**

```
touch process/tasks/my_module/some_task.py
touch process/tasks/my_module/test_some_task.py
```

**Registering a task:**

Run: `python manage.py create_task {module_name} {task_name}`. e.g.:

```
> python manage.py create_task foo bar
* Created: ./process/tasks/foo/__init__.py
* Created: ./process/tasks/foo/bar.py
* Created: ./process/tasks/foo/test_bar.py
```

In order to expose your task via the API, you will need to add it to `process/registry.py`

Now you will see your task in the registry endpoint at: `/docs/registry/tasks/`

## Processes

Processes combine a number of tasks in a well defined way to provide useful functionality.

Processes are `yml` files, and borrow a lot from [Ansible](https://ansible.com) in terms of how they are structured
Processes are stored in: `process/processes/`.

**A simple example process**

```
---
name: HelloWorld
description: Prints hello world
payload: []
tasks:
  - task: io.say_hello
```


**A complete example process**

```
---
name: SignupRequest
description: ...
payload:
  - key: username
    type: string
    required: true
    default: none
  - key: password
    type: string
    required: true
    validate:
      - "validation.min_length:8"
# validations will receive the payload as the first argument
validations:
  - validate_not_exists
tasks:
  - task: account.create_user
    args:
      username: payload.username
      password: payload.password
    # register will add the response of the task to the state of
    # the process. e.g.: the below will be accessible on: `state.user`
    register: user
# same as tasks but are run in the background:
# meaning:
# 1: they don't block
# 2: if they fail, they do not fail the process
tasks_async:
  - task: slack.send_notification
    args:
      message: "New user: {{state.user}}"
  - task: account.send_welcome_email
    args:
      user: state.user
# sheduled tasks run at a specified time in the future
tasks_scheduled:
  - task: account.send_follow_up_email
    args:
      user: state.user
    schedule:
      time: 5
      period: days # one of: mins, hours, days
      schedule: after # or before
      object: state.user
      field: signup_date

```


### Process API:

**Process:**

**POST /:process_id Create a process instance (e.g.: `POST /hello-world`)

**GET /:** List processess

**Documentation**

DJProcess builds documentation for you as you go.






