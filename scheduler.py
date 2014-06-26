# -*- coding: utf-8 -*-
# Check README.md and LICENSE for license stuff

import argparse
import httplib2
import os
import sys
import datetime
import time

from apiclient import discovery
from oauth2client import file
from oauth2client import client
from oauth2client import tools
from rfc3339 import rfc3339

secure_dir_no_git = "not-git-tracked-secure"
xrds_dir_no_git = "xrds-data"

days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
today=time.localtime().tm_wday
day=time.localtime().tm_mday
hour=time.localtime().tm_hour
month=time.localtime().tm_mon

CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), secure_dir_no_git+'/client_secrets.json')
FLOW = client.flow_from_clientsecrets(CLIENT_SECRETS,
  scope=[
      'https://www.googleapis.com/auth/calendar',
      'https://www.googleapis.com/auth/calendar.readonly',
    ],
    message=tools.message_if_missing(CLIENT_SECRETS))

with open(secure_dir_no_git+'/calendar_id.txt') as f:
    calendarID = f.readlines()
calendarID = str(calendarID[0]).replace('\n', "")		#ID of the google calendar to write the events to

def main(argv):
  
  with open(xrds_dir_no_git+'/bloggers.txt') as bloggers: 	#file to get the current bloggers from
	bloggers_data = bloggers.readlines()
  print("OK: Bloggers are -> " + bloggers_data)
  log = open(xrds_dir_no_git+"/schedule.txt", 'w') 		#file to output schedule to

  storage = file.Storage(secure_dir_no_git+'/sample.dat')
  credentials = storage.get()
  if credentials is None or credentials.invalid:
    credentials = tools.run_flow(FLOW, storage, flags)
  http = httplib2.Http()
  http = credentials.authorize(http)
  service = discovery.build('calendar', 'v3', http=http)

  try:
    print("OK: Probing for google / internet . . . ")

    while True:
        start_month_choice = raw_input("Which month to start (type number, jan=1, feb=2, ..., dec=12)")
        if start_month_choice.isdigit() and start_month_choice != "0" and int(start_month_choice)<13:
		start_month = months[int(start_month_choice)-1]
                print("OK: Starting month will be " + start_month)
		num_month_choice = raw_input("How many months to output?")
        	if num_month_choice.isdigit():
                		num_month = int(num_month_choice)
                		print("OK: Will calculate for  " + str(num_month) + " months")
				print len(bloggers_data)%(num_month*4)
				#if (len(bloggers_data)%(num_month*4)) != 0:
                		#	print("SORRY: " + str((len(bloggers_data)%num_month)) + " bloggers are left because with " + num_month + " you cannot do a full round robin")
				#	print("SORRY: Will continue bue if you want full round robin run again with different month setting")
			        s=0
				i=0
				while (s <= num_month * 4):
					if (i >= len(bloggers_data)):
						i = 0
					log.write(bloggers_data[i])
					event_summary=bloggers_data[i]	
        #event_start_time = datetime.time(int(d1[0]), int(d1[1]))
        #event_start_date = datetime.date(int(date_parsed[0]), int(date_parsed[1]), int(date_parsed[2]))
        #event_start = datetime.datetime.combine(event_start_date, event_start_time)
        #event_start = rfc3339(event_start)
        #event_end = event_start
					#1 9 16 23
					i+=1
					s+=1

    
    #print "--------------"
    #print "summary", event_summary
    #print "where", event_address   
    #print "start", event_start
    #print "end", event_end 
    #print "--------------"

    					event = {
   						'summary': '[XRDS] Blogging Assigment :)',
   						'location': "XRDS Blog at xrds.acm.org/blog/",
						'description': "Contribute your coolest idea to the blog: (1) write the draft (2) send for review (3) review and post it (4) help us advertise it!",
   						'start': {
   							'dateTime': "2014-08-07",
							'timeZone': "America/Los_Angeles"
    						},
    	#'end': {
	#	'dateTime': event_end,
#		'timeZone': "Europe/Berlin"
 #   	},
    						}

    					created_event = service.events().insert(calendarId=calendarID, body=event).execute()
    					print created_event['id']
	else:
		print("SORRY: Please next time specify month using a number")
    
    else:
	print("not adding to google cal") 
	#quit

  except client.AccessTokenRefreshError:
    print ("The credentials have been revoked or expired, please re-run"
      "the application to re-authorize")

if __name__ == '__main__':
  main(sys.argv)
