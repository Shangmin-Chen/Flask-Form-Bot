from keep_alive import keep_alive
from replit import db
import asyncio
from checking_time import check_six
import api
import Botv2

async def loop():
  # this segment is to see if theres nothing in database, wait until someone posts something into the database.
  while True:
    if "database" in db.keys():
      database = db["database"]
      print(str(database))
      break
    else:
      await asyncio.sleep(60)

  # Constant or init variables
  cool_down = 0
  
  while True:
    database = db["database"]
    value, reason, vdate = api.run_api()
    if check_six() == 0:
      # it's 6
      if cool_down == 0:
        # init run
        value, reason, vdate = api.run_api()
        if value == 0:
          total_time = Botv2.execute(database)
          print("Today's date is {}.\nTotal Run Time: {} seconds".format(vdate, str(total_time)))
          # make it go on cooldown
          cool_down = 1
    else:
      print("not 6")

    if cool_down == 0:
      print("ready")
      await asyncio.sleep(60)
    elif cool_down == 1:
      if check_six() == 1:
        # this makes sure that the code runs once at 6, and goes into cooldown. Once it's not 6, it goes off cooldown and becomes available again.
        cool_down = 0
        print("no longer 6")
        await asyncio.sleep(60)
      else:
        print("not ready")
        await asyncio.sleep(60)

keep_alive()
asyncio.run(loop())
