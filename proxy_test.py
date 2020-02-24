import socket
import socks
import requests


response = requests.get('http://icanhazip.com/', proxies={"socks5": "118.190.144.173:4211"})
print(response.text)
socks.set_default_proxy(socks.HTTP, "118.190.144.173", 4211)
socket.socket = socks.socksocket
service = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
service.connect((f'smtp.global-mail.cn', 25))
msg = service.recv(4096)
data = str(msg, encoding='utf-8').strip().split('\r\n')