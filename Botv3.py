import requests
import threading
import numpy as np
# this alogrithm makes it so sebby can go commercial.
url = "https://healthscreening.schools.nyc/home/submit"

def RUN(email, fname, lname):
    data = {
        "Type": "G",
        "IsOther": "False",
        "IsStudent": "1",
        "FirstName": fname,
        "LastName": lname,
        "Email": email,
        "State": "NY",
        "Location": "R605",
        "Floor": "",
        "Answer1": "0",
        "Answer2": "0",
        "Answer3": "0",
        "ConsentType": "",
    }

    response = requests.post(url, data=data).text
    print(response)

def insert(data_list, code):
  threads = []
  for i in data_list:
    fname = i[0]
    lname = i[1]
    email = i[2]
    t = threading.Thread(target=RUN, daemon=True, args=(email, fname.capitalize(), lname.capitalize()))
    threads.append(t)
  for i in range(len(data_list)):
    threads[i].start()

  for i in range(len(data_list)):
    threads[i].join()

def execute(data_list):
  length = len(data_list)

  threads = []
  
  a = float(length) / float(15)
  print("a={}".format(a))
  b = length // 15
  print("b={}".format(b))
  
  if a <= 1:
    insert(data_list, 0)

  elif a > b:
    b += 1
    data_list = np.array_split(data_list, b)
    for i in data_list:
      t = threading.Thread(target=insert, daemon=True, args=(i, 0))
      threads.append(t)

    for i in range(b):
      threads[i].start()

    for i in range(b):
      threads[i].join()

