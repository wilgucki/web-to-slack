import asyncio
import json
from typing import Union

from redis import Redis

from tornado.ioloop import IOLoop
from tornado.web import Application
from tornado.websocket import WebSocketHandler


redis_client = Redis(host='redis_db', port=6379, db=0)
ps = redis_client.pubsub(ignore_subscribe_messages=True)


class ChatHandler(WebSocketHandler):
    def initialize(self):
        ps.subscribe(**{'slack-to-web': self.pubsub_listener})
        ps.run_in_thread(sleep_time=0.001)

    def check_origin(self, origin: str) -> bool:
        return True

    def open(self, *args: str, **kwargs: str):
        print('open')

    def on_close(self):
        print('on_close')

    def on_message(self, message: Union[str, bytes]):
        print('received from website: ' + message)
        redis_client.publish('web-to-slack', message)

    def pubsub_listener(self, pubsub_message):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()

        asyncio.set_event_loop(loop)

        json_data = pubsub_message['data'].decode()
        data = json.loads(json_data)

        loop.run_until_complete(asyncio.wait([self.write_message(data)]))


if __name__ == '__main__':
    app = Application([
        (r'/chat', ChatHandler),
    ])
    app.listen(8888)

    IOLoop.current().start()
