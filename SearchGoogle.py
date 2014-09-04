import webapp2
import imp
import httplib2
import os
import sys
import json
import cloudstorage

import argparse
from datetime import datetime
from collections import namedtuple
#import tzlocal
#import pytz
from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client import client
from oauth2client.tools import run
from oauth2client.client import OAuth2WebServerFlow
import gflags


BusyBlock = namedtuple("BusyBlock", "year, month, day, startTime endTime")

# decorator = appengine.OAuth2DecoratorFromClientSecrets(
#   'client_secrets.json',
#   scope='https://www.googleapis.com/auth/calendar')
# 
FLAGS = gflags.FLAGS

FLOW = OAuth2WebServerFlow(
	client_id='867412132283-vk6grnslsq7uq3gsafe21v7f00blca5s.apps.googleusercontent.com',
	client_secret='01JZVBwcrmbJexziXRC-XS8S',
	scope=['https://www.googleapis.com/auth/calendar','https://www.googleapis.com/auth/calendar.readonly',],
	user_agent='folkloric-alpha-692/1')
# 	
# FLAGS.auth_local_webserver = False	
# 	
# storage = Storage('calendar.dat')
# credentials = storage.get()
# if credentials is None or credentials.invalid == True:
# 	credentials = run(FLOW, storage)
# 	
# http = httplib2.Http()
# http = credentials.authorize(http)
# 
# service = build(serviceName='calendar', version='v3', http=http,
# 	developerKey='AIzaSyCc4hQRQIGTy5jIgF0ca4E1HafAKqO2CYQ')	


def googleSearch(userId, startTimeParam, startDate, endTime, endDate):
  storage = Storage('calendar.dat')
  credentials = storage.get()
  if credentials is None or credentials.invalid == True:
	pass
	
  service = build(serviceName='calendar', version='v3',
    developerKey='AIzaSyCc4hQRQIGTy5jIgF0ca4E1HafAKqO2CYQ')		

  try:

    tz = "-0000"
    page_token = None

    myStartTime = startDate + "T" + startTimeParam + ":01" + tz
    #end time  string put together  add :00 for the seconds or else it fails
    myEndTime = endDate + "T" + endTime + ":00" + tz

    while True:
		#get the calendar id is always the onid plus this email or else it wont work
      calendarID = userId + "@gmail.com"
      #calendarID = "cs419.team4@gmail.com"

      startTime = "startTime"

      try:
		#order by the start time, have it all as single events, min and max time are our parameters we put in
		#also we are having it return in the time zone of the local machine, not useful for full day events but very helpful for datetime events
        events = service.events().list(calendarId=calendarID, pageToken=page_token, orderBy=startTime, singleEvents=True, timeMin=myStartTime, timeMax=myEndTime).execute()
      except:
	    #when we get an error from the events return, normally meaning a bad onid id
        events = "NoID"

#       def ld_writeDicts(filePath,events):
#         f=open(filePath, 'w')
#         newData = json.dumps(events,indent=4)
#         f.write(newData)
#         f.close()
# 
#       ld_writeDicts('/bucket/resultsjson/results.json', events)
# 
#         busyTimes = list()
# 
#       with open("/bucket/resultsjson/results.json") as json_file:
#         json_data = json.load(json_file)


      path = '/bucket/resultsjson/results.json'
	  source = CloudStorage.read(path)
	  source = source.decode('utf-8')
 	  content = content.encode('utf-8')
	  path = CloudStorage.normalize_path(path)
	  file_obj = cls.open(path, mode='w')
	  file_obj.write(events)
	  file_obj.close()		
		
		
	  filename = 'results.json'
	  json_data = cloudstorage.open(filename).read()

        i = -1
        for items in json_data['items']:
            n = i
            i +=1
            for key, value in items.iteritems():
                start = json_data['items'][n]['start']
                start1 = str(start)
                if len(start1) == 43:
                    st1 = start1[16:32]
                    year = st1[0:4]
                    month = st1[5:7]
                    day = st1[8:10]
                    sHour = st1[11:13]
                    sMin =  st1[14:16]
                    startTime = sHour + sMin
                if len(start1) == 24:
                    st1 = start1[12:22]
                    year = st1[0:4]
                    month = st1[5:7]
                    day = st1[8:10]
                    #sHour = st1[12:13]
                    #sMin =  st1[14:15]
                    startTime = "0000"
                end = json_data['items'][n]['end']
                end1 = str(end)
                if len(end1) == 43:
                    en1 = end1[16:32]
                    eYear = en1[0:4]
                    eMonth = en1[5:7]
                    eDay = en1[8:10]
                    eHour = en1[11:13]
                    eMin =  en1[14:16]
                    endTime = eHour + eMin
                if len(end1) == 24:
                    en1 = end1[12:28]
                    eYear = en1[0:4]
                    eMonth = en1[5:7]
                    eDay = en1[8:10]
                    #eHour = en1[11:13]
                    #eMin =  en1[14:16]
                    endTime = "0000"

            print year, month, day, startTime, eYear, eYear, eMonth, eDay, endTime

            #busyBlock = BusyBlock(year, month, day, startTime, endTime)
            #busyTimes.append(busyBlock)
        #return busyTimes

      if not page_token:
        break

  except client.AccessTokenRefreshError:
    pass

  return events

#if __name__ == '__main__':

class MainHandler(webapp2.RequestHandler):

		userId = "rezalution786"

		startYear = "2014"
		startMonth = "08"
		startDay =  "30"
		startDate = startYear + "-" + startMonth + "-" + startDay
		startDate = str(startDate)

		startHour = "00"
		startMin =  "00"
		startTimeParam = startHour + ":" + startMin
		startTimeParam = str(startTimeParam)

		endHour = "00"
		endMin = "00"
		endTime = endHour + ":" + endMin
		endTime = str(endTime)

		endYear = "2014"
		endMonth = "09"
		endDay =  "02"
		endDate = endYear + "-" + endMonth + "-" + endDay
		endDate = str(endDate)

		googleSearch(userId, startTimeParam, startDate, endTime, endDate)
  
application = webapp2.WSGIApplication(
	[('/', MainHandler)], 
	debug=True)
