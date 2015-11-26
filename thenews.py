"""
Send the top 20 posts in /r/all every time this runs.

Plan: run this every 8 hours in cron
"""
import smtplib
from email.mime.text import MIMEText

import uuid
from ConfigParser import SafeConfigParser
import time
import datetime

import pprint

import pytz
import requests, requests.auth

# handle UTF-8 correctly in stdout/stderr
import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)


reddit_all = "https://oauth.reddit.com/r/all/top"

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
    oauth2_token = r.json()
else:
    raise Exception("No Authorization token! Why?")

request_headers = dict()
request_headers['Authorization'] = 'bearer ' + oauth2_token['access_token']
request_headers['User-Agent'] = session_user_agent

request_data = dict()
request_data['limit'] = 100

time.sleep(3)
r = requests.get(reddit_all, headers=request_headers, params=request_data)

if r.ok:
    news = r.json()
else:
    raise("There was a problem with the request, status code: {}".format(r.status_code))

display_keys = ['title', 'score', 'permalink', 'subreddit', 'id', 'created_utc']

display_content = dict()
for entry in news['data']['children']:
    current_id = entry['data']['id']
    display_content[current_id] = dict() 
    for data_field in display_keys:
        display_content[current_id][data_field] = entry['data'][data_field]

    # this would probably work but the server may use a different local than pacific.
    # print datetime.datetime.fromtimestamp(entry['data']['created_utc'])
    display_content[current_id]['created_localtime'] = pytz.timezone('US/Pacific').localize(datetime.datetime.fromtimestamp(entry['data']['created_utc'])).strftime('%H:%M:%S %m/%d/%Y')

# use display_keys to handle the manufactured string too
display_keys.append('created_localtime')

CONTENT = u""

for k, v in display_content.iteritems():
    CONTENT += u"{} ".format(k,)
    for data_field in display_keys:
        CONTENT += u"{} ".format(v[data_field],)
    CONTENT += u"\n"

print CONTENT


me = 'robbintt@gmail.com'
you = 'robbintt@gmail.com'

msg = MIMEText(CONTENT, 'plain', 'UTF-8')

msg['Subject'] = "The Subject, DATE"
msg['From'] = me
msg['To'] = you

s = smtplib.SMTP('localhost')
s.sendmail(me, [you], msg.as_string())

# this is a good candidate for a context manager
s.quit
