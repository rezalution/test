import gflags
import httplib2
#from apiclient.discovery import build
#from apiclient import discovery
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run
# Contact to client
FLOW = OAuth2WebServerFlow(
	client_id='867412132283-vk6grnslsq7uq3gsafe21v7f00blca5s.apps.googleusercontent.com',
	client_secret='01JZVBwcrmbJexziXRC-XS8S',
	scope='https://www.googleapis.com/auth/calendar',
	user_agent='folkloric-alpha-692')
# create storage if offline
storage = Storage('calendar.dat')
credentials = storage.get()	
if credentials is None or credentials.invalid == True:
	credentials = run(FLOW, storage)
# authorize
http = httplib2.Http()
http = credentials.authorize(http)
service = build(serviceName='calendar', version='v3', http=http,
	developerKey='AIzaSyCc4hQRQIGTy5jIgF0ca4E1HafAKqO2CYQ')