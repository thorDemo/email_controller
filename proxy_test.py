import socket
import socks
import requests
import urllib3


response = requests.get('http://icanhazip.com/', proxies={"http": "http://190.2.144.46:18006"})
print(response.text)
# print(0)
socks.set_default_proxy(socks.HTTP, "190.2.144.46", 18006)
socket.socket = socks.socksocket
service = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
service.connect(('smtp.global-mail.cn', 25))
print(1)
msg = service.recv(4096)
data = str(msg, encoding='utf-8').strip().split('\r\n')
# s = urllib3.connection_from_url('http://icanhazip.com/')
