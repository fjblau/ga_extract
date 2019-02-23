"""Hello Analytics Reporting API V4."""

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import json
import mysql.connector as mysql


SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = 'client_secrets.json'
VIEW_ID = '189627627'


def initialize_analyticsreporting():
  """Initializes an Analytics Reporting API V4 service object.

  Returns:
    An authorized Analytics Reporting API V4 service object.
  """
  credentials = ServiceAccountCredentials.from_json_keyfile_name(
      KEY_FILE_LOCATION, SCOPES)

  # Build the service object.
  analytics = build('analyticsreporting', 'v4', credentials=credentials)

  return analytics


def initialize_mysql():

  db = mysql.connect(
    host = "localhost",
    user = "wx",
    passwd = "wx"
    )
  cursor = db.cursor()
  print("Database Open")
  return cursor

def get_report(analytics): 
  """Queries the Analytics Reporting API V4.

  Args:
    analytics: An authorized Analytics Reporting API V4 service object.
  Returns:
    The Analytics Reporting API V4 response.
  """
  return analytics.reports().batchGet(
      body={
        'reportRequests': [
        {
          'viewId': VIEW_ID,
          'dateRanges': [{'startDate': '3daysAgo', 'endDate': 'today'}],
          'metrics': [ {'expression': 'ga:pageviews'} ],
          'dimensions': [{'name': 'ga:channelGrouping'}, {'name': 'ga:date'}]
        }]
      }
  ).execute()


def print_response(response):
  rowcount = int(json.dumps(response['reports'][0]['data']['rowCount']))
  print (rowcount)
  r = json.dumps(response['reports'][0]['data']['rows'])
 
  metric = json.loads(r)
  for i in range (0, rowcount):
    source = json.dumps(metric[i]['dimensions'][0]).replace('"', '')
    date = json.dumps(metric[i]['dimensions'][1]).replace('"', '')
    m = json.dumps(metric[i]['metrics'][0]['values'][0]).replace('"', '')
    #print (int(m.replace('"','')))
    print(source, date, int(m))

  #output = json.loads(r['reports'][0])
  #pj = json.dumps(output, indent=4, sort_keys=True)
  #print (pj)

  """Parses and prints the Analytics Reporting API V4 response.

  Args:
    response: An Analytics Reporting API V4 response.
  """


def main():
  database = initialize_mysql()
  analytics = initialize_analyticsreporting()
  response = get_report(analytics)
  print_response(response)

if __name__ == '__main__':
  main()