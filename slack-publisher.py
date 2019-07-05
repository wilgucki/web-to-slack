"""Publish message to slack

Should be run as daemon
"""
import json
import os
import time

import slack
from dotenv import load_dotenv
from redis import Redis


load_dotenv()

redis_client = Redis(host='redis_db', port=6379, db=0)
ps = redis_client.pubsub(ignore_subscribe_messages=True)
ps.subscribe('web-to-slack')

slack_client = slack.WebClient(token=os.environ['SLACK_API_TOKEN'])

while True:
    message = ps.get_message()
    if message:
        json_message = json.loads(message['data'].decode())
        slack_client.chat_postMessage(
            channel='#client-notifications',
            text=json_message['message']
        )

    time.sleep(0.01)
