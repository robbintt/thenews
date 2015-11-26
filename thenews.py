"""
Send the top 20 posts in /r/all every time this runs.

Plan: run this every 8 hours in cron
"""
import smtplib
from email.mime.text import MIMEText
import uuid
from ConfigParser import SafeConfigParser
import requests, requests.auth

reddit_request_token = "https://www.reddit.com/api/v1/access_token"

session_user_agent = "simple personal news monitor:" + str(uuid.uuid4())

config_filename = 'secret.cfg'
config = SafeConfigParser()
config.read(config_filename)
secret = config.get('app', 'secret')
appid = config.get('app', 'id')
username = config.get('app', 'username')
username_p = config.get('app', 'username_p')

headers = dict()
headers['User-Agent'] = session_user_agent

post_data = dict()
post_data['grant_type'] = 'password'
post_data['username'] = username
post_data['password'] = username_p


client_auth = requests.auth.HTTPBasicAuth(appid, secret)

r = requests.post(reddit_request_token, headers=headers, auth=client_auth, data=post_data)

if r.ok:
    print r.json()


reddit_all = "https://www.reddit.com/r/all/"


'''
headers = dict()
headers['t'] = 'hour'
headers['User-Agent'] = str(uuid.uuid4()) + " simple personal news monitor"
headers[''] = appid
'''

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
