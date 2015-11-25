"""
Send the top 20 posts in /r/all every time this runs.

Plan: run this every 8 hours in cron
"""
import smtplib
from email.mime.text import MIMEText
import uuid

import requests

reddit_all = "https://www.reddit.com/r/all/"

headers = dict()
headers['t'] = 'hour'
headers['User-Agent'] = uuid.uuid4()

r = requests.get(reddit_all, headers=headers)

"""
me = 'robbintt@gmail.com'
you = 'robbintt@gmail.com'

with open(textfile, 'rb') as fp:
    msg = MIMEText(fp.read)

msg['Subject'] = "The Subject, DATE"
msg['From'] = me
msg['To'] = you

s = smtplib.SMTP('localhost')
s.sendmail(me, [you], msg.as_string())

# this is a good candidate for a context manager
s.quit
"""
