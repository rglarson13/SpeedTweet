#!/usr/bin/env python

# you're gonna wanna:
# pip install tweepy

import tweepy

# I figured out how to tweet with Python from here:
# http://nodotcom.org/python-twitter-tutorial.html

def get_api(cfg):
  auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
  auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
  return tweepy.API(auth)

def sendtweet(tweet, image_path = ""):
  # Fill in the values noted in previous step here
  cfg = { 
    "consumer_key"        : "Get",
    "consumer_secret"     : "these",
    "access_token"        : "from",
    "access_token_secret" : "Twitter" 
    }
	#Create an app on Twitter: https://apps.twitter.com/
	#Documentation from Twitter: https://dev.twitter.com/oauth/reference/post/oauth/access_token

  api = get_api(cfg)
  
  if image_path == "":
    status = api.update_status(status=tweet) 
  else:
    status = api.update_with_media(image_path, tweet) # for images


# I'm using this guy's SpeedTest python script to generate the results log:
# https://github.com/sivel/speedtest-cli
	
import csv

data = open("speedtest.csv", "r").read().splitlines()

rows = csv.reader(data, quotechar = '"', delimiter = ",", quoting = csv.QUOTE_ALL)

speeds = []
for row in rows:
	speeds.append(row)

# Server ID - 0,Sponsor - 1,Server Name - 2,Timestamp - 3,Distance - 4,Ping - 5,Download - 6,Upload - 7

slowcount = []
fastcount = 0
badcount = 0
rownum = 0

# this is inelegant, but it works well enough and it's still only 10 lines
while len(slowcount) < 4:

	rownum = rownum + 1

	if len(speeds[rownum]) == 8:
		downspeed = round((float(speeds[rownum][6]) / (1024)) / 1024,1)

		# I picked 25 mbps, but if you want a different number you'll wanna change this
		if downspeed > 25:
			break
		else:
			slowcount.append(downspeed)
	else:
		badcount = badcount + 1


if len(slowcount) == 4:

	maxspeed = 0
	
	for slowspeed in slowcount:
		if slowspeed > maxspeed:
			maxspeed = slowspeed

	sendtweet("@comcast My speeds top out at " + str(maxspeed) + " mbps. Paying for more than twice that. #NotGettingWhatIPayFor #ComcastIsSlow")