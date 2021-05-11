import os

import requests


def send_telegram_message(bot_message):
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    bot_chat_id = os.getenv('TELEGRAM_BOT_CHAT_ID')
    if bot_token is None or bot_chat_id is None:
        raise ValueError("Please set TELEGRAM_BOT_TOKEN and TELEGRAM_BOT_CHAT_ID as env variables")

    bot_api = "https://api.telegram.org/bot{0}/sendMessage?chat_id={1}&parse_mode=Markdown&text={2}"
    send_message = bot_api.format(bot_token, bot_chat_id, bot_message)
    try:
        response = requests.get(send_message)
        response.raise_for_status()
    except requests.HTTPError as http_error:
        print(http_error.response.content)
