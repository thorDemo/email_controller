from mylib.long_connect import SMTPSocket
from email.mime.text import MIMEText
from email.header import Header
from mylib.code_logging import Logger as Log
from mylib.coder import encode_header
from mylib.tools import rand_from, rand_to, rand_title
import uuid

log = Log('send_email.log').get_log()

sender = 'china@jshongze.com'
password = 'pyri10%ec'

receivers = list()
service = SMTPSocket(log, sender, password)
service.debuglevel = 1
service.socket_connect()
service.auth_user()
content = open('templates/type_2.html', encoding='utf-8')
message = MIMEText(content.read(), _subtype='html', _charset='utf-8')

file = open('target/1.txt', 'r', encoding='utf-8')
temp = 1
for email in file:
    receivers.append(email.strip())
    if temp % 10 == 0:
        receivers.append('914081010@qq.com')
        message['Accept-Language'] = "zh-CN"
        message['Accept-Charset'] = "ISO-8859-1,UTF-8"
        message['From'] = encode_header(rand_from(), sender)
        message['To'] = encode_header(rand_to(), receivers)
        message['Subject'] = Header(rand_title(), 'utf-8')
        message['Received'] = f'from msc-channel180022225.sh(180.97.229.111) by heqibo@ggecs.com(127.0.0.1);'
        message['Message-ID'] = uuid.uuid4().__str__()
        message['MIME-Version'] = '1.0'
        message['Return-Path'] = sender
        service.send_mail(sender, receivers, message.as_bytes())
        receivers = []
    temp += 1
