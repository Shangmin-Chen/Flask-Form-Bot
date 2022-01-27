# Using NYC 311 Public Developers api key to check if school is opened
import os
import requests
import json
from checking_time import check_day

KEY = os.environ['APIKEY']

def run_api():
  m, d, y = check_day()
  vdate = "{}/{}/{}".format(m, d, y)
  try:
    r = requests.get("https://api.nyc.gov/public/api/GetCalendar?fromdate={}&todate={}".format(vdate, vdate), headers={"Ocp-Apim-Subscription-Key": KEY})
  except:
    # the 9's here are fills for the argument because main.py is expecting 3 arguments
    return 1, 1, 9

  if r.status_code == 200:
    # connected/ good
    data = json.loads(r.text)
    status = data["days"][0]["items"][2]["status"]
    reason = data["days"][0]["items"][2]["details"]
  else:
    return 1, 2, 9

  if status == "OPEN":
  # open/ true return 0
    return 0, reason, vdate

