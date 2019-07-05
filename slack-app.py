import json
import os
import datetime

from dotenv import load_dotenv
from redis import Redis
from slackeventsapi import SlackEventAdapter


load_dotenv()
redis_client = Redis(host='redis_db', port=6379, db=0)

slack_events_adapter = SlackEventAdapter(os.environ['SLACK_SIGNING_SECRET'], endpoint='/slack/events')


def message(event_data):
    if 'text' not in event_data['event']:
        return

    if 'username' in event_data['event'] and event_data['event']['username'] == 'webslack':
        return

    msg = {
        'author': 'site admin',
        'date': str(datetime.datetime.now()),
        'message': event_data['event']['text']
    }

    redis_client.publish('slack-to-web', json.dumps(msg))


slack_events_adapter.on('message', message)
slack_events_adapter.start(host='0.0.0.0', port=3000, debug=True)
