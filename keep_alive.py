from flask import Flask, render_template, request
from threading import Thread
from replit import db

app = Flask(__name__)

@app.route('/')
def home():
  return render_template("index.html")

@app.route('/', methods=['POST'])
def my_form_post():
  if request.method == "POST":
    fname = request.form["First"]
    lname = request.form["Last"]
    email = request.form["Mail"]
    yn = request.form["yesno"]

    if yn == "Delete":
      database = db["database"]
      count = 0
      for i in database:
        count += 1
        for j in i:
          if email in j:
            del database[count-1]
            db["database"] = database
            data = (fname.capitalize(), lname.capitalize())
            return render_template("successdel.html", data=data)

    elif "" == fname or "" == lname or "" == email or "" == yn:
      return render_template("emptyerror.html")
    
    elif "@" not in email:
      return render_template("mailerror.html")

    else:
      database = db["database"]
      for i in database:
        for j in i:
          if email in j:
            data = email
            return render_template("alreadyexist.html", data=data)

    print("New user registered: {} {} {}".format(fname, lname, email))

    if "database" in db.keys():
      database = db["database"]
      data = [fname, lname, email]
      database.append(data)
      db["database"] = database        
      data = (fname.capitalize(), lname.capitalize())
      return render_template("successadd.html", data=data)
    else:
      database = []
      data = [[fname, lname, email]]
      db["database"] = data
      data = (fname.capitalize(), lname.capitalize())
      return render_template("successadd.html", data=data)

def run():
  app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
