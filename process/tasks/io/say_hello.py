__simple_example = '''
- task: process.tasks.slack.send_message
  args:
    message: 'hello!'
'''
__meta = {
    'args': {
        'message': { 'type': 'str', 'default': 'hello world'},
    },
    'examples': [
        { 'title': 'Basic usage', 'description': __simple_example },
    ]
}

def say_hello(message='hello world', *args, **kwargs):
    '''Prints `message` or "hello world" if no message is provied'''

    print(message)
    return {'result': message}