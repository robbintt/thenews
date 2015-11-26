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

import pytz
import requests, requests.auth


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

#pprint.pprint(news)
#[pprint.pprint(x['data']['url']) for x in news['data']['children']]
#[pprint.pprint(x['data'].keys()) for x in news['data']['children']]
#[pprint.pprint(x['data']['title']) for x in news['data']['children']]

for entry in news['data']['children']:
    print entry['data']['title']
    print entry['data']['score']
    print entry['data']['permalink']
    print entry['data']['subreddit']
    print entry['data']['id']
    print pytz.timezone('US/Pacific').localize(datetime.datetime.fromtimestamp(entry['data']['created_utc']))
    # this would probably work but the server may use a different local than pacific.
    # print datetime.datetime.fromtimestamp(entry['data']['created_utc'])


"""
print news
print news.keys()

print 

#print news['kind']

print news['data'].keys()
print news['data']['after']
print news['data']['before']
"""


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
