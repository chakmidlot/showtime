import requests

from showtime import settings

SEND_MESSAGE_URL = "{}/bot{}/sendMessage"


def send(user, message):
    send_url = SEND_MESSAGE_URL.format(settings.TELEGRAM_HOST, settings.TELEGRAM_TOKEN)

    data = {
        "chat_id": user,
        "text": message
    }
    requests.post(send_url, data=data)
