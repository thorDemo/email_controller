import socket
import socks
import requests


response = requests.get('http://icanhazip.com/', proxies={"http": "58.218.92.76:2513"})
print(response.text)
socks.set_default_proxy(socks.SOCKS5, "58.218.92.76", 2513)
socket.socket = socks.socksocket
service = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
service.connect((f'smtp.global-mail.cn', 25))
msg = service.recv(4096)
data = str(msg, encoding='utf-8').strip().split('\r\n')
print(data)