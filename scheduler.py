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
newline = '\n'

days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
weeks = [1, 9, 16, 23]
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
  print("OK: Bloggers are -> ", bloggers_data)
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

    start_month_choice = raw_input("Which month to start (type number, jan=1, feb=2, ..., dec=12)")
    if start_month_choice.isdigit() and start_month_choice != "0" and int(start_month_choice)<13:
	start_month = months[int(start_month_choice)-1]
        print("OK: Starting month will be " + start_month)
	num_weeks_choice = raw_input("How many weeks to output?")
        if num_weeks_choice.isdigit():
        	num_weeks = int(num_weeks_choice)
               	print("OK: Will calculate for  " + str(num_weeks) + " weeks")
		if ((num_weeks)%len(bloggers_data) != 0):
               		print("SORRY: needed to schedule " + str((num_weeks)%len(bloggers_data)) + "more bloggers so you can have a full round robin with only " + str(num_weeks) + " weeks.")
			print("SORRY: Will continue but if you want full round robin run again with different month setting")
		s=0
		start_mon = int(start_month_choice)
		start_day = 1
        	event_start_date = datetime.date(datetime.datetime.now().year,start_mon,start_day)
        	start_day_o = event_start_date.toordinal() 
		i=0
		week = 1
		#log.write("\t\t"+ months[start_mon-1] + newline)
		#print("\t\t"+ months[start_mon-1] + newline)
		while (s < num_weeks):
			if (i >= len(bloggers_data)):
				i = 0
			name = str(bloggers_data[i]).replace('\n', '')
			#log.write(name+"\t\t"+ "week " + str(week) + newline)
			#print(name+"\t\t"+ "week " + str(week) + newline)
			event_summary=bloggers_data[i]	
			#start_counts_date = event_start_date

			if (week-1 > 0):
				start_day_o = start_day_o  + 7 - (datetime.date.fromordinal(start_day_o)).weekday()
			print (datetime.date.fromordinal(start_day_o))
        		
			event_start_time = datetime.time(int("18"), int("00"))
        		event_start_date = datetime.date.fromordinal(start_day_o)
        		event_start = datetime.datetime.combine(event_start_date, event_start_time)
        		event_start = rfc3339(event_start)
        		event_end_time = datetime.time(int("20"), int("00"))
        		event_end = datetime.datetime.combine(event_start_date, event_end_time)
        		event_end = rfc3339(event_end)
			i+=1
			s+=1
			week+=1
    			event = {
   				'summary': '[XRDS] Blogging Assigment for ' + name,
   				'location': "XRDS Blog at xrds.acm.org/blog/",
				'description': "Contribute your coolest idea to the blog: (1) write the draft (2) send for review (3) review and post it (4) help us advertise it!",
   				'start': {
   					'dateTime': event_start,
					'timeZone': "America/Los_Angeles"
    				},
    				'end': {
					'dateTime': event_end,
					'timeZone': "America/Los_Angeles"
 			   	},
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
