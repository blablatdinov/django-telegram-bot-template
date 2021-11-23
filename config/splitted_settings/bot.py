import os
from collections import namedtuple

import requests
from loguru import logger
from requests.exceptions import ConnectionError

TG_BOT = namedtuple('Bot', ['token', 'webhook_host', 'name', 'id'])
TG_BOT.token = os.getenv('BOT_TOKEN')
TG_BOT.webhook_host = os.getenv('HOST')

try:
    r = requests.get(f'https://api.telegram.org/bot{TG_BOT.token}/getMe').json()
    if not r.get('ok'):
        raise Exception('Data in .env is not valid')
    TG_BOT.name = r['result']['username']
    TG_BOT.id = r['result']['id']
except ConnectionError:
    pass

try:
    if os.getenv('ADMINS') == '':
        TG_BOT.admins = []
    else:
        TG_BOT.admins = [int(chat_id) for chat_id in os.getenv('ADMINS').split(',')]
except (ValueError, AttributeError):
    logger.warning('Пожалуйста проверьте переменную ADMINS в файле .env')
    exit(1)
