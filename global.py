from mylib.login_test import SMTPSocket
from email.mime.text import MIMEText
from email.header import Header
from mylib.code_logging import Logger as Log
from mylib.coder import encode_header
from mylib.tools import rand_from, rand_to, rand_title
import uuid
import time
from mylib.tools import rand_account

log = Log('send_email.log').get_log()

file = open('target/1.txt', 'r', encoding='utf-8')
temp = 0
for line in file:
    receivers = line.strip()
    username, password = rand_account()
    sender = username
    service = SMTPSocket(log, username, password)
    service.debuglevel = 1
    content = open('templates/type_2.html', encoding='utf-8')
    message = MIMEText(content.read(), _subtype='html', _charset='utf-8')
    message['Accept-Language'] = "zh-CN"
    message['Accept-Charset'] = "ISO-8859-1,UTF-8"
    message['From'] = encode_header(rand_from(), sender)
    message['To'] = encode_header(rand_to(), receivers)
    message['Subject'] = Header(rand_title(), 'utf-8')
    message['Received'] = f'from msc-channel180022225.sh(180.97.229.111) by heqibo@ggecs.com(127.0.0.1);'
    message['Message-ID'] = uuid.uuid4().__str__()
    message['MIME-Version'] = '1.0'
    message['Return-Path'] = sender
    service.send_mail(sender, receivers, message.as_string())
    if temp % 100 == 0:
        receivers = '914081010@qq.com'
        username, password = rand_account()
        sender = username
        service = SMTPSocket(log, username, password)
        service.debuglevel = 1
        content = open('templates/type_2.html', encoding='utf-8')
        message = MIMEText(content.read(), _subtype='html', _charset='utf-8')
        message['Accept-Language'] = "zh-CN"
        message['Accept-Charset'] = "ISO-8859-1,UTF-8"
        message['From'] = encode_header(rand_from(), sender)
        message['To'] = encode_header(rand_to(), receivers)
        message['Subject'] = Header(f'回测邮件{temp}', 'utf-8')
        message['Received'] = f'from msc-channel180022225.sh(180.97.229.111) by heqibo@ggecs.com(127.0.0.1);'
        message['Message-ID'] = uuid.uuid4().__str__()
        message['MIME-Version'] = '1.0'
        message['Return-Path'] = sender
        service.send_mail(sender, receivers, message.as_string())
    temp += 1
