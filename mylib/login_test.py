#! /usr/bin/env python3
import socket
import dns.resolver
from logging import Logger
from base64 import b64encode


__all__ = ["SMTPException", "SMTPReplyError", "SMTPServerDisconnected", "SMTPSocket"]


class SMTPException(OSError):
    """base exception 基础异常类"""


class SMTPReplyError(SMTPException):
    """reply message error 返回消息异常"""


class SMTPServerDisconnected(SMTPException):
    """disconnection error 连接失败"""


SMTP_PORT = 25
CRLF = "\r\n"
bCRLF = b"\r\n"
_MAXLINE = 8192     # more than 8 times larger than RFC 821, 4.5.3
ACCOUNT = 'heqibo@ggecs.com'
PASSWORD = 'Ptyw1q2w3e$R'


class SMTPSocket:
    debuglevel = 0

    def __init__(self, logging: Logger, username, password):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.service = object
        self.domain = object
        self.logging = logging
        self.username = username
        self.password = password

    def send_mail(self, sender, receivers, message):
        # type: (str, str, str) -> (int, str)
        """
        :param sender :
        :param receivers:
        :param message:
        :return:
        """
        try:
            self.domain = self.username.split('@')[1]
            connect = self.socket_connect()
            if connect is False:
                return 0, 'mail box not exist!'
            # code, msg = self.helo()
            # if code == 521:
            #     return 0, msg
            self.helo()
            self.ehlo()
            self.auth_login()
            self.mail_from(sender)
            code, msg = self.mail_rcpt(receivers)
            if code != 250:
                return code, msg
            message = bytes(message, encoding='utf-8')
            code, msg = self.send_data(message)
            return code, msg
        except SMTPException as e:
            self.logging.warning(f'{e}')
            return 0, 'send error'
        except TimeoutError:
            self.logging.warning('connect timeout!')
            return 0, 'connect timeout!'

    def socket_connect(self):
        # preference, exchange, recode = self.query_mx()
        # if preference == 0:
        #     return False
        self.service = f'smtp.global-mail.cn'
        if self.debuglevel > 0:
            self.logging.debug(f'> Connect: smtp.global-mail.cn')
        self.socket.connect((f'smtp.global-mail.cn', SMTP_PORT))
        code, msg = self.get_reply()
        if code != 220:
            self.socket_close()
            raise SMTPServerDisconnected(msg)
        return True

    def query_mx(self):
        try:
            mx = dns.resolver.query(self.domain, 'MX')
            preference = 0
            exchange = ''
            recode = []
            for i in mx:
                if self.debuglevel == 1:
                    self.logging.debug(f'> dns:{i.preference}{i.exchange}')
                if int(i.preference) > preference:
                    recode.append({i.preference, i.exchange})
                    preference = i.preference
                    exchange = str(i.exchange).strip('.')
            return preference, exchange, recode
        except dns.resolver.NXDOMAIN:
            return 0, '', []

    def helo(self):
        request = f'HELO global-mail.cn{CRLF}'
        if self.debuglevel > 0:
            self.logging.debug(f'> HELO global-mail.cn')
        self.socket.sendall(str(request).encode('utf-8'))
        code, msg = self.get_reply()
        if code == -1 and len(msg) == 0:
            self.socket_close()
            raise SMTPServerDisconnected
        if code == 250:
            return code, msg
        elif code == 521:
            return code, f'sohu {msg}'
        else:
            self.socket_close()
            raise SMTPReplyError(code, msg)

    def ehlo(self):
        request = f'EHLO global-mail.cn{CRLF}'
        if self.debuglevel > 0:
            self.logging.debug(f'> EHLO global-mail.cn')
        self.socket.sendall(str(request).encode('utf-8'))
        code, msg = self.get_reply()
        if code == -1 and len(msg) == 0:
            self.socket_close()
            raise SMTPServerDisconnected
        if code == 250:
            return code, msg
        else:
            self.socket_close()
            raise SMTPReplyError(code, msg)

    def auth_login(self):
        user = str(b64encode(bytes(self.username, encoding='utf-8')), 'utf-8')
        self.logging.debug(f'> RANDOM ACCOUNT {self.username}')
        self.send_command(f'AUTH LOGIN {user}')
        password = str(b64encode(bytes(self.password, encoding='utf-8')), 'utf-8')
        self.send_command(password)

    def send_command(self, data):
        request = f'{data} {CRLF}'
        if self.debuglevel > 0:
            self.logging.debug(f'> {data}')
        self.socket.sendall(str(request).encode('utf-8'))
        c, m = self.get_reply()
        return c, m

    def mail_from(self, sender):
        request = f'MAIL FROM:<{sender}>{CRLF}'
        if self.debuglevel > 0:
            self.logging.debug(f'> MAIL FROM:<{sender}>')
        self.socket.sendall(str(request).encode('utf-8'))
        code, msg = self.get_reply()
        if code == 250:
            return code, msg
        else:
            self.socket_close()
            raise SMTPReplyError(code, msg)

    def mail_rcpt(self, receivers):
        request = f'RCPT TO:<{receivers}>{CRLF}'
        if self.debuglevel > 0:
            self.logging.debug(f'> RCPT TO:<{receivers}>')
        self.socket.sendall(str(request).encode('utf-8'))
        code, msg = self.get_reply()
        if code == 250:
            return code, msg
        else:
            self.socket_close()
            return code, msg

    def send_data(self, message):
        request = f'DATA{CRLF}'
        if self.debuglevel > 0:
            self.logging.debug(f'> DATA string')
            self.logging.debug(f'> {message}')
        self.socket.sendall(request.encode('utf-8'))
        code, msg = self.get_reply()
        if code == 354:
            self.socket.send(message + b'\r\n.\r\n')
            code, msg = self.get_reply()
            if code == 250:
                self.socket_close()
                return code, msg
            else:
                return code, str(msg)
        else:
            self.socket_close()
            return code, msg

    def socket_close(self):
        request = f'QUIT{CRLF}'
        if self.debuglevel > 0:
            self.logging.debug(f'> QUIT')
        self.socket.sendall(str(request).encode('utf-8'))
        code, msg = self.get_reply()
        self.socket.close()
        if code == 221:
            return code, msg
        else:
            return -1, ''

    def get_reply(self):
        msg = self.socket.recv(4096)
        if self.debuglevel > 0:
            data = str(msg, encoding='utf-8').split('\r\n')
            for line in data:
                self.logging.debug(f'< {line}')
        if len(msg) > 0:
            data = str(msg, encoding='utf-8').split('\r\n')
            if 'sohu' in self.service:
                for line in data:
                    if line[3:4] == '-':
                        temp_data = line.split('-')
                        message = ' '.join(temp_data[1:8])
                        code = temp_data[0]
                        return int(code), message
                    elif line[3:4] == ' ':
                        temp_data = line.split(' ')
                        message = ' '.join(temp_data[1:8])
                        code = temp_data[0]
                        return int(code), message
            else:
                for line in data:
                    if line[3:4] == ' ':
                        temp_data = line.split(' ')
                        message = ' '.join(temp_data[1:8])
                        code = temp_data[0]
                        return int(code), message
            raise SMTPReplyError
        else:
            raise SMTPReplyError
