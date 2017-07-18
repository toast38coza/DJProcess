import os
from slackclient import SlackClient

__simple_example = """
  - task: process.tasks.slack.send_message
    args:
      message: 'hello!'
      channel: 'notifications'
"""

__meta = {
    'args': {
        'message': { 'type': 'str', 'required': True},
        'channel': { 'type': 'str', 'default': 'general'},
    },
    'examples': [
        { 'title': 'Basic usage', 'description': __simple_example },
    ],
    "requirements": [
        'slackclient==1.0.5'
    ]
}

def send_message(message, channel='general', **kwargs):
    '''Send a message to slack
    * Payload: { message: '...', channel: '...' }
    '''
    token = os.environ.get('SLACK_TOKEN')
    slack_client = SlackClient(token)
    return slack_client.api_call("chat.postMessage", channel=channel, text=message)
