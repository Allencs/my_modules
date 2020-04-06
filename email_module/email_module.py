import socket
from email.header import Header
import TickerConfig
from email.mime.text import MIMEText
import smtplib


class Email(object):

    message = None

    subject = ""

    def __init__(self):
        try:
            self.sender = TickerConfig.EMAIL_CONF["email"]
            self.receiver = TickerConfig.EMAIL_CONF["notice_email_list"]
            self.username = TickerConfig.EMAIL_CONF["username"]
            self.password = TickerConfig.EMAIL_CONF["password"]
            self.host = TickerConfig.EMAIL_CONF["host"]
        except Exception as e:
            print(u"邮件配"
                  u"置有误{}".format(e))

    def create_subject(self, subject):
        self.subject = subject

    def create_message(self, message):
        self.message = MIMEText(message, 'plain', 'utf-8')  # 中文需参数‘utf-8’，单字节字符不需要
        self.message['Subject'] = Header(self.subject, 'utf-8')
        self.message['From'] = self.sender
        self.message['To'] = self.receiver

    def send(self):
        try:
            smtp = smtplib.SMTP_SSL(self.host, 994)
            smtp.connect(self.host)
        except socket.error:
            smtp = smtplib.SMTP()
            smtp.connect(self.host)
        smtp.connect(self.host)
        smtp.login(self.username, self.password)
        smtp.sendmail(self.sender, self.receiver.split(","), self.message.as_string())
        smtp.quit()
        print(u"------邮件已通知, 请查收------")


if __name__ == '__main__':
    newEmail = Email()
    newEmail.create_subject("")
    newEmail.create_message("")
    newEmail.send()



