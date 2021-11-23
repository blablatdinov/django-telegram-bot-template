from collections import namedtuple

import requests
from requests.exceptions import ConnectionError

from config.splitted_settings.environ import env

TG_BOT = namedtuple('Bot', ['token', 'webhook_host', 'name', 'id'])
TG_BOT.token = env('BOT_TOKEN')
TG_BOT.webhook_host = env('HOST')

try:
    r = requests.get(f'https://api.telegram.org/bot{TG_BOT.token}/getMe').json()
    if not r.get('ok'):
        raise Exception('Data in .env is not valid')
    TG_BOT.name = r['result']['username']
    TG_BOT.id = r['result']['id']
except ConnectionError:
    pass

TG_BOT.admins = list(map(int, env('ADMINS', list)))
