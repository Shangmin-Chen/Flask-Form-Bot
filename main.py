from keep_alive import keep_alive
from replit import db
import asyncio
from checking_time import check_six
import api
import Botv3

for i in range(len(db["database"])):
  print(str(i+1), db["database"][i][0], db["database"][i][1])
  
# this loop will be async
async def loop():
  # this segment is to see if theres nothing in database, wait until someone posts something into the database.
  while True:
    if "database" in db.keys():
      database = db["database"]
      break
    else:
      await asyncio.sleep(60)

  # Constant or init variables
  cool_down = 0
  
  while True:
    if check_six() == 0:
      # it's 6
      if cool_down == 0:
        # init run
        value, reason, vdate = api.run_api()

        try:
          database = db["database"]
        except Exception as e:
          print(e)

        if value == 1:
          # 1 and 1 means that theres a connection error, and the solution is to try to reconnect again 3 more times in 60 second intervals.
          for i in range(3):
            await asyncio.sleep(60)
            value, reason, vdate = api.run_api()
            if value == 0:
              # if it connected then break the loop
              print("connected")
              break

        if value == 0:
          try:
            Botv3.execute(database)
          except Exception as e:
            print(e)
          print("Running... Today's date is {}, {}.".format(vdate, reason))
          # make it go on cooldown
          cool_down = 1

        elif value == 2: # school closed
          print("School closed... Today's date is {}, {}.".format(vdate, reason))
        
        elif value == 1 and reason == 1:
          # this is an api down error
          print("connection error")
          exit()

        elif value == 1 and reason == 2:
          # this is an api down error
          print("404 error")
          exit()

    if cool_down == 0:
      # ready
      await asyncio.sleep(60)

    # if ran already at 6
    elif cool_down == 1:
      if check_six() == 1:
        # this makes sure that the code runs once at 6, and goes into cooldown. Once it's not 6, it goes off cooldown and becomes available again.
        cool_down = 0
        # no longer 6
        await asyncio.sleep(60)
      else:
        # not ready
        await asyncio.sleep(60)

keep_alive()
asyncio.run(loop())
