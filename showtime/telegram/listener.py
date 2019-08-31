import time
import logging
import traceback
import re

import requests

from showtime import settings
from showtime.db import DB
from showtime.telegram.commands import Commands
from showtime.telegram.sender import send

logger = logging.getLogger(__name__)


UPDATES_URL = "{}/bot{}/getUpdates?offset={{}}&timeout=20"


class Telergam:

    def __init__(self):
        self.db = DB()
        self.session = requests.Session()
        self.update_url = UPDATES_URL.format(settings.TELEGRAM_HOST, settings.TELEGRAM_TOKEN)
        self.update_id = self.db.get_telegram_checkpoint("APP_NAME") or 0

        self.commands = Commands()

        self.command_pattern = re.compile("/(\w+) ?(.*)")

    def get_updates(self):
        while True:
            try:
                resonse = self.session.get(self.update_url.format(self.update_id)).json()
                if resonse['ok']:
                    messages = [x['message'] for x in resonse['result'] if 'message' in x]
                    for query in messages:
                        response = self.parse_message(query)
                        if response:
                            send(query['chat']['id'], response)

                    if len(resonse['result']):
                        self.update_id = resonse['result'][-1]['update_id'] + 1
                        self.db.set_telegram_checkpoint(settings.APP_NAME, self.update_id)
                else:
                    logger.warning("Not ok. " + resonse['description'])
                    time.sleep(10)

            except Exception as e:
                logger.warning(traceback.format_exc())
                time.sleep(10)

    def parse_message(self, message):
        if 'text' in message:
            match = self.command_pattern.match(message['text'])

            if match:
                command_name, data = match.groups()
                command = getattr(self.commands, command_name)
                if command:
                    return command(message['chat']['id'], data)


if __name__ == '__main__':
    Telergam().get_updates()
