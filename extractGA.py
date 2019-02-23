"""Hello Analytics Reporting API V4."""

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import json
import mysql.connector as mysql
from mysql.connector import Error
from datetime import datetime


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


def get_report(analytics): 
 
  return analytics.reports().batchGet(
      body={
        'reportRequests': [
        {
          'viewId': VIEW_ID,
          'dateRanges': [{'startDate': '3daysAgo', 'endDate': 'today'}],
          'metrics': [ {'expression': 'ga:pageviews'} ],
          'dimensions': [{'name': 'ga:source'}, {'name': 'ga:date'}]
        }]
      }
  ).execute()


def insert_response(response):
  rowcount = int(json.dumps(response['reports'][0]['data']['rowCount']))
  r = json.dumps(response['reports'][0]['data']['rows'])
  print(r)
  db = mysql.connect(user='wx', password='wx', host='localhost', port='3306', database='ga') 
  if db.is_connected:
    print("DB isConnected")
  cursor = db.cursor()
  

  metric = json.loads(r)
  for i in range (0, rowcount):

    source = json.dumps(metric[i]['dimensions'][0]).replace('"', '')
    date = json.dumps(metric[i]['dimensions'][1]).replace('"', '')
    m = json.dumps(metric[i]['metrics'][0]['values'][0]).replace('"', '')
    mysqldate  = datetime.strptime(date, '%Y%m%d').date()
    sql = "insert into ga(ga_date, source, metric) values(%s, %s, %s)"
    val = (mysqldate, source, int(m))
    cursor.execute(sql, val)
    db.commit()
    

def main():
  analytics = initialize_analyticsreporting()
  response = get_report(analytics)
  insert_response(response)

if __name__ == '__main__':
  main()