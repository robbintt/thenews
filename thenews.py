"""
Send the top 100 posts in /r/all every time this runs.

Future:
    allow prioritization of certain subreddits if they exist.
    for example, worldnews is always slot #1 and science is always slot #2
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
secret = config.get('redditapp', 'secret')
appid = config.get('redditapp', 'id')
username = config.get('reddit', 'username')
username_p = config.get('reddit', 'username_p')
gmail_email = config.get('email', 'email')
gmail_password = config.get('email', 'password')

target_recepient = config.get('recepient', 'email')
ignored_subreddits = config.get('subreddits', 'ignored').split("|")
priority_subreddits = config.get('subreddits', 'priority').split("|")

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
request_data['t'] = 'day'
request_data['show'] = 'all'


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
    display_content[current_id]['created_localtime'] = pytz.timezone('US/Pacific').localize(datetime.datetime.fromtimestamp(entry['data']['created_utc'])).strftime('%H:%M %m/%d')
    display_content[current_id]['full_permalink'] = "http://www.reddit.com/"+entry['data']['permalink']

# use display_keys to handle the manufactured string too
display_keys.append('created_localtime')
display_keys.append('full_permalink')

# make a set of all subreddits in top posts
display_subreddits = list()
for k,v in display_content.iteritems():
    if v['subreddit'] not in display_subreddits:
        display_subreddits.append(v['subreddit'])
display_subreddits = sorted(display_subreddits, key=unicode.lower)

# smash priority_subreddits on the front of display_subreddits
display_subreddits = [subr for subr in display_subreddits if subr not in priority_subreddits]
display_subreddits = priority_subreddits + display_subreddits
    

CONTENT = u""
CONTENT += u"<HTML><HEAD></HEAD><BODY>"

# filter posts from each subreddit one at a time
for subreddit in display_subreddits:
    if subreddit not in ignored_subreddits:
        subreddit_filtered_display_content = dict( [ (filt_k, filt_v) for filt_k, filt_v in display_content.iteritems() if filt_v['subreddit'] == subreddit ] )
        CONTENT += "<H4>{}</H4>".format(subreddit)
        for k, v in subreddit_filtered_display_content.iteritems():
            CONTENT += u"<DIV style='padding: 5px;'>"
            CONTENT += u"<a target='_blank' href='{}'>{}</a>".format(v['full_permalink'], v['title'])
            CONTENT += u" | {} ".format(v['created_localtime'],)
            CONTENT += u" | score: {} ".format(v['score'],)
            CONTENT += u"</DIV>"
        CONTENT += u"</BODY></HTML>"

msg = MIMEText(CONTENT, 'html', 'UTF-8')
msg['Subject'] = "Top Posts Today: /r/all in the last 24h - {} Pacific/US".format(datetime.datetime.now().strftime('%H:%M %m/%d/%Y'))
msg['From'] = gmail_email
msg['To'] = target_recepient

#s = smtplib.SMTP('localhost', 1025) # test port
s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls()
s.login(gmail_email, gmail_password)
s.sendmail(gmail_email, [target_recepient], msg.as_string())

# this is a good candidate for a context manager
s.quit
