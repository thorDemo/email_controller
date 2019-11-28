import requests
import uuid
from mylib.coder import encode_header
from email.mime.text import MIMEText
from mylib.tools import rand_from, rand_to, rand_title
from email.header import Header
import dkim


def mime_msg(sender, receivers, dkim_selector, dkim_key, service_ip, title=None):
    # type: (str, str, str, str, str, str) -> str
    if title is None:
        title = rand_title()
    domain = sender.split('@')[1]
    fh = open(dkim_key)
    dkim_key = fh.read()
    fh.close()
    content = open('templates/type_1.html', encoding='utf-8')
    message = MIMEText(content.read(), _subtype='html', _charset='utf-8')
    content.close()
    message['Accept-Language'] = "zh-CN"
    message['Accept-Charset'] = "ISO-8859-1,UTF-8"
    message['From'] = encode_header(rand_from(), sender)
    message['To'] = encode_header(rand_to(), receivers)
    message['Subject'] = Header(title, 'utf-8')
    message['Received'] = f'from msc-channel180022225.sh({service_ip}) by mail.{domain}(127.0.0.1);'
    message['Message-ID'] = uuid.uuid4().__str__()
    message['MIME-Version'] = '1.0'
    message['Return-Path'] = f'mail.{domain}'
    signature = dkim.sign(
        message=message.as_bytes(),
        selector=bytes(dkim_selector, encoding='utf-8'),
        domain=bytes(domain, encoding='utf-8'),
        privkey=bytes(dkim_key, encoding='utf-8'),
    )
    message['DKIM-Signature'] = bytes.decode(signature.lstrip(b"DKIM-Signature: "))
    return message.as_bytes()
