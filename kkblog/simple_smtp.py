# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText


def simple_smtp_send(username, password, server, to_list, subject, content):
    '''
简易的为gmail准备的smtp发邮件函数
注意，当前python必须支持ssl
argument:
    username即欲登录的邮箱名。
return:
    1:successfully
    2:can't login server
    3:error occurs when sending mail
'''
    me = "%s<%s>" % (username, username)
    msg = MIMEText(content, _charset="utf-8")
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        s = smtplib.SMTP()
        s.connect(server)
        s.ehlo()  # for gmail
        s.starttls()  # for gmail
        s.login(username, password)
    except:
        return 2
    try:
        s.sendmail(me, to_list, msg.as_string().encode("utf-8"))
        s.close()
    except:
        return 3
    return 1
