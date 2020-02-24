import requests
from mylib.smtp_message import mime_msg
from mylib.code_logging import Logger
import time
import json

stream = open('conf/pontirest.com.json')
config = json.load(stream)
logging = Logger('send_email.log').get_log()
service = config['service']
sender = f'service@{config["domain"]}'
dkim_key = config['dkim_key']
dkim_selector = config['dkim_selector']
file = open(config['target'], encoding='utf-8')
temp = 0
for line in file:
    if temp % config['return_delay'] == 0:
        receivers = config['return_box']
        return_title = f'{service} > %5d' % temp
        result = mime_msg(sender, receivers, 's1', dkim_key, '23.88.229.127', return_title)
        data = {
            'sender': sender,
            'receivers': receivers,
            'message': result,
        }
        response = requests.post(f'http://{service}:5000/post/office/', data=data)
        if response.status_code == 200:
            reply = response.json()
            logging.info(f'{temp} - return mail box - {reply["code"]} - {reply["msg"]}')
        time.sleep(config['delay'])

    receivers = line.strip()
    result = mime_msg(sender, receivers, dkim_selector, dkim_key, '23.88.229.183')
    data = {
        'sender': sender,
        'receivers': receivers,
        'message': result,
    }
    response = requests.post(f'http://{service}:5000/post/office/', data=data)
    if response.status_code == 200:
        reply = response.json()
        logging.info(f'{temp} - {receivers} - {reply["code"]} - {reply["msg"]}')
    time.sleep(config['delay'])
    temp += 1
